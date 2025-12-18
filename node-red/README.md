# Fluxos Node-RED

Esta pasta contém os fluxos desenvolvidos no Node-RED, responsáveis pela integração, processamento e visualização dos dados coletados no sistema de monitoramento inteligente do orquidário.

O Node-RED atua como o núcleo de orquestração do sistema, conectando os dispositivos IoT, o banco de dados e a camada de inteligência artificial.

---

## 📌 Funcionalidades dos Fluxos

Os fluxos implementados desempenham as seguintes funções:

- Recepção de dados ambientais via protocolo MQTT
- Processamento e validação das leituras dos sensores
- Armazenamento das leituras em banco de dados MongoDB
- Gerenciamento de perfis de cultivo
- Integração com a camada de Inteligência Artificial
- Exibição de dashboards para monitoramento em tempo real e análise histórica

---

## 🔗 Integrações

- **MQTT**  
  Recebe dados de telemetria publicados pelo ESP32 no tópico:


- **MongoDB**  
Armazena séries temporais de dados ambientais e informações de perfis de cultivo.

- **Inteligência Artificial**  
Recebe recomendações geradas pela IA por meio do tópico:


---

## 📊 Dashboards

Os dashboards desenvolvidos permitem:

- Visualização em tempo real das variáveis ambientais
- Consulta ao histórico de medições
- Exibição de alertas e recomendações da IA
- Gestão de perfis de cultivo

---

## 📥 Importação dos Fluxos

Para importar os fluxos no Node-RED:

1. Acesse o Node-RED
2. Clique no menu ☰
3. Selecione **Import → Clipboard**
4. Cole o conteúdo do arquivo `flows.json`
5. Clique em **Import**

---

## ⚠️ Observações Importantes

- As credenciais de acesso (MQTT e MongoDB) devem ser configuradas pelo usuário.
- Os fluxos foram desenvolvidos para execução em servidor local.
- Os dashboards utilizam componentes do Node-RED Dashboard.

---

## 🎓 Contexto Acadêmico

Estes fluxos fazem parte do Trabalho de Conclusão de Curso (TCC) apresentado ao Instituto Federal de São Paulo (IFSP), no curso de Pós-Graduação em Internet das Coisas (IoT).

