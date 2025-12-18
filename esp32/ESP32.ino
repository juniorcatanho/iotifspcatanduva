#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHTesp.h>
#include <Wire.h>
#include <BH1750.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <WiFiManager.h>
#include <EEPROM.h>
#include <ArduinoJson.h>

// --- Definições de Pinos ---
#define PINO_DHT 13
#define PINO_UMIDADE_SOLO_A0 34 

// --- Configurações MQTT Broker ---
char mqtt_server[40] = ""; // IP da sua VPS
const int mqtt_port = 1883;
const char* mqtt_user = "";
const char* mqtt_pass = "";

// --- Tópicos MQTT ---
const char* mqtt_topic_telemetria = "estufa/dados/telemetria";
const char* mqtt_topic_status_conexao = "estufa/status/conexao";
const char* mqtt_topic_controle_comando = "estufa/controle/comando";

// --- Variáveis de Calibração ---
const int UMIDADE_SOLO_SECO_VALOR = 4095; 
const int UMIDADE_SOLO_MOLHADO_VALOR = 2000;

// --- Variáveis Globais ---
WiFiClient espClient;
PubSubClient client(espClient);
DHTesp dht;
BH1750 lightMeter;
WiFiUDP ntpUdp;
NTPClient timeClient(ntpUdp, "pool.ntp.org", -3 * 3600, 60000);

float temperatura = 0.0;
float umidadeAr = 0.0;
float luminosidadeLux = 0.0;
int umidadeSolo = 0; 

// Intervalos
const long SENSOR_READ_INTERVAL_MS = 60000; 
unsigned long lastSensorReadTime = 0;

// --- FUNÇÕES PARA SALVAR/CARREGAR CONFIGURAÇÃO ---
void saveConfig() {
  StaticJsonDocument<256> doc;
  doc["mqtt_server"] = mqtt_server;

  char jsonBuffer[256];
  serializeJson(doc, jsonBuffer);

  EEPROM.begin(512);
  EEPROM.writeString(0, jsonBuffer);
  EEPROM.commit();
  EEPROM.end();
  Serial.println("Configurações salvas na EEPROM.");
}

void loadConfig() {
  EEPROM.begin(512);
  String jsonStr = EEPROM.readString(0);
  EEPROM.end();

  if (jsonStr.length() > 0) {
    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, jsonStr);
    if (error) {
      Serial.println("Falha ao ler o JSON da EEPROM, usando valores padrão.");
    } else {
      strlcpy(mqtt_server, doc["mqtt_server"] | "24.199.99.30", sizeof(mqtt_server));
      Serial.println("Configurações carregadas da EEPROM.");
    }
  } else {
    Serial.println("Nenhuma configuração encontrada na EEPROM, usando valores padrão.");
  }
}

// --- LÓGICA DO WIFI MANAGER (CHAMADA APENAS QUANDO NECESSÁRIO) ---
void startConfigPortal() {
  WiFiManager wm;

  WiFiManagerParameter custom_mqtt_server("server", "IP do Servidor MQTT", mqtt_server, 40);
  wm.addParameter(&custom_mqtt_server);
  
  wm.setSaveConfigCallback([&]() {
      Serial.println("Configuração salva pelo portal. O ESP32 será reiniciado.");
      strlcpy(mqtt_server, custom_mqtt_server.getValue(), sizeof(mqtt_server));
      saveConfig();
      ESP.restart();
  });
  
  // Define um tempo limite para o portal de configuração
  wm.setConfigPortalTimeout(180); // 3 minutos

  Serial.println("Iniciando portal de configuração...");
  if (!wm.startConfigPortal("Estufa-Config")) {
    Serial.println("Falha ao conectar e o tempo expirou. Reiniciando...");
    delay(3000);
    ESP.restart();
    delay(5000);
  }
  
  // Se chegou aqui, significa que o usuário salvou as configs pelo portal
  // e o ESP32 irá reiniciar por causa do callback.
}


// --- Funções de Conexão ---
void reconnectMQTT() {
    while (!client.connected()) {
        Serial.print("Conectando ao MQTT...");
        if (client.connect("ESP32_Estufa_01", mqtt_user, mqtt_pass, mqtt_topic_status_conexao, 1, true, "OFFLINE")) {
            Serial.println("Conectado ao MQTT!");
            client.subscribe(mqtt_topic_controle_comando);
            client.publish(mqtt_topic_status_conexao, "ONLINE", true);
        } else {
            Serial.print("Falha na conexão MQTT, rc=");
            Serial.print(client.state());
            Serial.println(" Tentando novamente em 5s...");
            delay(5000);
        }
    }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Mensagem MQTT recebida no tópico: ");
    Serial.println(topic);
    String message = "";
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    Serial.print("Conteúdo: ");
    Serial.println(message);
    if (String(topic) == mqtt_topic_controle_comando) {
        if (message == "reset_esp") {
            Serial.println("Comando de reset recebido. Reiniciando ESP32...");
            ESP.restart();
        }
    }
}

// --- Funções de Leitura e Publicação ---
int lerValorEstavelDoSensor(int pino) {
    int total = 0;
    int numeroDeLeituras = 20;
    for (int i = 0; i < numeroDeLeituras; i++) {
        total += analogRead(pino);
        delay(5);
    }
    return total / numeroDeLeituras;
}

void readAndPublishSensors() {
    temperatura = dht.getTemperature();
    umidadeAr = dht.getHumidity();
    luminosidadeLux = lightMeter.readLightLevel();
    
    int valorBrutoSolo = lerValorEstavelDoSensor(PINO_UMIDADE_SOLO_A0);
    umidadeSolo = map(valorBrutoSolo, UMIDADE_SOLO_SECO_VALOR, UMIDADE_SOLO_MOLHADO_VALOR, 0, 100);
    umidadeSolo = constrain(umidadeSolo, 0, 100);

    if (isnan(temperatura) || isnan(umidadeAr)) {
        Serial.println("Falha ao ler do sensor DHT!");
        return;
    }
    
    timeClient.update();
    String timestamp = timeClient.getFormattedTime();

    char jsonPayload[256];
    snprintf(jsonPayload, sizeof(jsonPayload),
             "{\"timestamp\":\"%s\",\"temperatura\":%.1f,\"umidade_ar\":%.1f,\"umidade_solo\":%d,\"luminosidade_lux\":%.0f}",
             timestamp.c_str(),
             temperatura,
             umidadeAr,
             umidadeSolo,
             luminosidadeLux);

    Serial.print("Publicando no MQTT: ");
    Serial.println(jsonPayload);
    client.publish(mqtt_topic_telemetria, jsonPayload);
}

// --- Setup Principal ---
void setup() {
    Serial.begin(115200);
    Serial.println("\nIniciando sistema de monitoramento...");
    
    // Inicia a memória não-volátil
    EEPROM.begin(512);

    // Carrega as configurações salvas (como o IP do MQTT)
    loadConfig();

    // Tenta se conectar ao WiFi conhecido
    WiFi.mode(WIFI_STA);
    WiFi.begin(); // Tenta conectar com as credenciais salvas
    
    Serial.print("Tentando conectar ao WiFi salvo...");
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 30) { // Tenta por ~15 segundos
        delay(500);
        Serial.print(".");
        attempts++;
    }

    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("\nNão foi possível conectar ao WiFi salvo. Iniciando portal de configuração.");
        startConfigPortal(); // Se falhar, inicia o portal
    }
    
    Serial.println("\nWiFi CONECTADO!");
    Serial.print("Endereco IP: ");
    Serial.println(WiFi.localIP());

    // O resto da inicialização...
    timeClient.begin();
    
    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(mqttCallback);

    dht.setup(PINO_DHT, DHTesp::DHT22);
    Wire.begin();
    lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE);
    
    Serial.println("Sistema inicializado.");
}

// --- Loop Principal ---
void loop() {
    if (!client.connected()) {
        reconnectMQTT();
    }
    client.loop();

    unsigned long currentTime = millis();
    if (currentTime - lastSensorReadTime >= SENSOR_READ_INTERVAL_MS) {
        lastSensorReadTime = currentTime;
        readAndPublishSensors();
    }
    
    delay(10);
}