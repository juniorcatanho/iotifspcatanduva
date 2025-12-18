# Firmware ESP32

Firmware responsável pela coleta de dados ambientais no orquidário.

## Sensores utilizados
- DHT22 (temperatura e umidade do ar)
- BH1750 (luminosidade)
- HD-38 (umidade do solo)

## Comunicação
- Protocolo MQTT
- Publica dados no tópico:
  - estufa/dados/telemetria

## Observação
As credenciais de rede e MQTT devem ser configuradas pelo usuário.
