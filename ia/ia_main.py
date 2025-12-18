import paho.mqtt.client as mqtt
import pymongo
import json
from datetime import datetime
import pandas as pd
import joblib
import os
import requests
import threading
import time
from bson.objectid import ObjectId

# --- CONFIGURAÇÕES ---
MONGO_CONNECTION_STRING = ""
MONGO_DB_NAME = "iotdb"
MONGO_COLLECTION_PERFIS = "perfis_cultura"

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_USER = ""
MQTT_PASS = ""
MQTT_CLIENT_ID = "Python_IA_Estufa_TCC"
MQTT_TOPIC_TELEMETRIA = "estufa/dados/telemetria"
MQTT_TOPIC_CULTIVO_ATIVO = "estufa/config/cultivo_ativo"
MQTT_TOPIC_RECOMENDACOES = "estufa/ia/recomendacoes"

WEATHER_API_KEY = ""
WEATHER_API_CITY = ""

# --- VARIÁVEIS GLOBAIS ---
mongo_client = None
db = None
perfil_ativo = None
modelo_anomalia = None
estatisticas_normalidade = None

clima_externo_atual = {}

# --- FUNÇÕES DE INICIALIZAÇÃO ---
def connect_to_mongo():
    global mongo_client, db
    try:
        mongo_client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
        db = mongo_client[MONGO_DB_NAME]
        print("Conectado ao MongoDB com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        db = None

def carregar_modelo_ml():
    global modelo_anomalia
    try:
        # *** ALTERAÇÃO AQUI ***
        nome_arquivo = 'modelo_anomalia_v2.pkl' 
        if os.path.exists(nome_arquivo):
            modelo_anomalia = joblib.load(nome_arquivo)
            print(f"Modelo de Machine Learning '{nome_arquivo}' carregado com sucesso!")
        else:
            print(f"AVISO: Arquivo do modelo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Erro ao carregar o modelo de Machine Learning: {e}")

def carregar_estatisticas():
    global estatisticas_normalidade
    try:
        # *** ALTERAÇÃO AQUI ***
        nome_arquivo = 'estatisticas_normalidade_v2.json'
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, 'r') as f:
                estatisticas_normalidade = json.load(f)
            print(f"Arquivo de estatísticas '{nome_arquivo}' carregado com sucesso!")
        else:
            print(f"AVISO: Arquivo de estatísticas '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Erro ao carregar o ficheiro de estatísticas: {e}")

def buscar_clima_externo():
    global clima_externo_atual
    url = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_API_CITY}&appid={WEATHER_API_KEY}&units=metric&lang=pt_br"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        clima_externo_atual = {
            "cidade": data.get('name', 'N/A'),
            "descricao": data['weather'][0]['description'],
            "temp": data['main']['temp'],
            "umid": data['main']['humidity']
        }
        print(f"Clima Externo Coletado: {clima_externo_atual['descricao'].upper()}, Temp: {clima_externo_atual['temp']}°C, Umid: {clima_externo_atual['umid']}%")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar clima externo: {e}")

def thread_busca_clima():
    while True:
        buscar_clima_externo()
        time.sleep(900) # Busca o clima a cada 15 minutos

# --- FUNÇÕES DE LÓGICA ---
def carregar_perfil_ativo(perfil_id):
    global perfil_ativo
    if db is None: return
    try:
        obj_id = ObjectId(perfil_id)
        perfil = db[MONGO_COLLECTION_PERFIS].find_one({"_id": obj_id})
        if perfil:
            perfil_ativo = perfil
            print(f"Perfil de cultivo '{perfil.get('nome_cultura', 'N/A')}' carregado.")
            client.publish(MQTT_TOPIC_RECOMENDACOES, json.dumps({
                "alerts": [f"Perfil '{perfil.get('nome_cultura', 'N/A')}' ativado."],
                "recommendation": "Aguardando novos dados dos sensores para análise."
            }))
        else:
            perfil_ativo = None
    except Exception as e:
        print(f"Erro ao carregar perfil do MongoDB: {e}")
        perfil_ativo = None

def explicar_anomalia(dados_atuais, hora_str):
    if not estatisticas_normalidade:
        return "Desvio de padrão detectado (análise detalhada indisponível)."

    estatisticas_hora = estatisticas_normalidade.get(hora_str, {})
    maior_desvio = {"sensor": "N/A", "valor": 0}

    for sensor, valor_atual in dados_atuais.items():
        if sensor in estatisticas_hora:
            stats = estatisticas_hora[sensor]
            media = stats.get('media', 0)
            desvio_padrao = stats.get('desvio_padrao', 0)

            if desvio_padrao > 0:
                num_desvios = abs(valor_atual - media) / desvio_padrao
                if num_desvios > maior_desvio["valor"]:
                    maior_desvio["sensor"] = sensor
                    maior_desvio["valor"] = num_desvios
    
    if maior_desvio["valor"] > 2.5: # Limiar de 2.5 desvios padrão
        sensor_culpado = maior_desvio['sensor'].replace('_', ' ').title()
        return f"ANOMALIA DETETADA: O valor de '{sensor_culpado}' está significativamente fora do padrão esperado para esta hora do dia."
    
    return "ANOMALIA DETETADA: Desvio de padrão detectado na correlação entre os sensores."


def generate_recommendations(data, clima_externo):
    rule_alerts = []
    ml_recommendation = "Nenhum desvio de padrão detectado."
    
    hora_atual = int(data.get('timestamp').split(':')[0])

    if modelo_anomalia:
        try:
            dados_para_predicao = {
                'temperatura': data.get('temperatura'),
                'umidade_ar': data.get('umidade_ar'),
                'umidade_solo': data.get('umidade_solo'),
                'luminosidade_lux': data.get('luminosidade_lux')
            }
            df_predicao = pd.DataFrame([dados_para_predicao])
            df_predicao['hora_do_dia'] = hora_atual
            
            colunas_treino = ['temperatura', 'umidade_ar', 'umidade_solo', 'luminosidade_lux', 'hora_do_dia']
            predicao = modelo_anomalia.predict(df_predicao[colunas_treino])
            
            if predicao[0] == -1:
                ml_recommendation = explicar_anomalia(dados_para_predicao, str(hora_atual))
        except Exception as e:
            print(f"Erro na predição do modelo de anomalia: {e}")

    if perfil_ativo is None:
        return {"alerts": ["Nenhum perfil de cultivo ativo."], "recommendation": "Selecione um cultivo no dashboard."}

    contexto_externo = ""
    if clima_externo:
        cidade = clima_externo.get('cidade', 'N/A')
        temp_ext = clima_externo.get('temp', 'N/A')
        umid_ext = clima_externo.get('umid', 'N/A')
        contexto_externo = f" (Condições em {cidade}: {temp_ext}°C, {umid_ext}% umid.)"

    if not (perfil_ativo['temperatura_ideal_min_C'] <= data['temperatura'] <= perfil_ativo['temperatura_ideal_max_C']):
        rule_alerts.append(f"ALERTA (Temp): {data['temperatura']}°C fora do ideal ({perfil_ativo['temperatura_ideal_min_C']}-{perfil_ativo['temperatura_ideal_max_C']}°C).{contexto_externo}")
    
    if not (perfil_ativo['umidade_ar_ideal_min_percent'] <= data['umidade_ar'] <= perfil_ativo['umidade_ar_ideal_max_percent']):
        rule_alerts.append(f"ALERTA (Umid Ar): {data['umidade_ar']}% fora do ideal ({perfil_ativo['umidade_ar_ideal_min_percent']}-{perfil_ativo['umidade_ar_ideal_max_percent']}%).{contexto_externo}")
    
    if not (perfil_ativo['umidade_solo_ideal_min_percent'] <= data['umidade_solo'] <= perfil_ativo['umidade_solo_ideal_max_percent']):
        rule_alerts.append(f"ALERTA (Umid Solo): {data['umidade_solo']}% fora do ideal ({perfil_ativo['umidade_solo_ideal_min_percent']}-{perfil_ativo['umidade_solo_ideal_max_percent']}%).")

    if not (6 <= hora_atual < 19):
        rule_alerts.append(f"Status (Lum): {data['luminosidade_lux']} Lux (Período noturno).")
    elif not (perfil_ativo['luminosidade_ideal_min_lux'] <= data['luminosidade_lux'] <= perfil_ativo['luminosidade_ideal_max_lux']):
        rule_alerts.append(f"ALERTA (Lum): {data['luminosidade_lux']} Lux fora do ideal ({perfil_ativo['luminosidade_ideal_min_lux']}-{perfil_ativo['luminosidade_ideal_max_lux']} Lux).")

    if not rule_alerts:
        rule_alerts.append("Status: Todos os parâmetros estão dentro dos limites ideais.")
            
    return {"alerts": rule_alerts, "recommendation": ml_recommendation}

# --- FUNÇÕES DE CALLBACK MQTT ---
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
        client.subscribe(MQTT_TOPIC_TELEMETRIA)
        client.subscribe(MQTT_TOPIC_CULTIVO_ATIVO)
    else:
        print(f"Falha na conexão com o MQTT, código: {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode('utf-8')
        if msg.topic == MQTT_TOPIC_CULTIVO_ATIVO:
            carregar_perfil_ativo(payload_str)
            return
        if msg.topic == MQTT_TOPIC_TELEMETRIA:
            data = json.loads(payload_str)
            recomendacao_obj = generate_recommendations(data, clima_externo_atual)
            client.publish(MQTT_TOPIC_RECOMENDACOES, json.dumps(recomendacao_obj))
            print(f"Publicando recomendação: {recomendacao_obj}")
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

# --- INICIALIZAÇÃO ---
if __name__ == "__main__":
    connect_to_mongo()
    carregar_modelo_ml()
    carregar_estatisticas()
    
    clima_thread = threading.Thread(target=thread_busca_clima, daemon=True)
    clima_thread.start()
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except Exception as e:
        print(f"Não foi possível conectar ao broker MQTT: {e}")
