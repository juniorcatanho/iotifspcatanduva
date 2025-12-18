# Monitoramento Inteligente em Orquidário de Pequenos Cultivadores

Este repositório reúne os códigos-fonte, fluxos, scripts e materiais complementares desenvolvidos no Trabalho de Conclusão de Curso (TCC) intitulado **“Monitoramento Inteligente em Orquidário de Pequenos Cultivadores”**, apresentado ao **Instituto Federal de São Paulo (IFSP)**, no curso de **Pós-Graduação em Internet das Coisas (IoT)**.

O projeto propõe uma solução de monitoramento ambiental inteligente voltada a pequenos produtores de orquídeas, integrando **Internet das Coisas (IoT)**, **processamento em servidor local**, **inteligência artificial híbrida** e **análise estatística**, com foco em baixo custo, explicabilidade e aplicabilidade prática.

---

## 🎓 Instituição

Instituto Federal de São Paulo – IFSP  Campus Catanduva
Curso de Pós-Graduação em Internet das Coisas (IoT)

---

## 👨‍💻 Autores

- **José Emílio Catanho da Silva Júnior**  
- **Anderson Jesus de Arruda**

---

## 📌 Contexto e Motivação

O cultivo de orquídeas é altamente sensível a variações ambientais, como temperatura, umidade do ar, umidade do solo e luminosidade. Pequenos produtores, em geral, não dispõem de ferramentas tecnológicas acessíveis que permitam o acompanhamento contínuo dessas variáveis, o que pode resultar em estresse fisiológico das plantas, doenças e perdas produtivas.

Nesse contexto, este trabalho busca oferecer uma alternativa tecnológica acessível, baseada em sensores IoT e análise inteligente dos dados coletados, permitindo:
- Monitoramento contínuo (24/7)
- Registro histórico confiável
- Detecção de desvios ambientais
- Apoio à tomada de decisão do produtor

---

## 🎯 Objetivo Geral

Desenvolver um sistema inteligente de monitoramento ambiental para orquidários, integrando sensores IoT, comunicação MQTT, processamento em servidor local e inteligência artificial híbrida, visando auxiliar pequenos cultivadores na gestão das condições ambientais.

---

## 🎯 Objetivos Específicos

- Implementar a coleta de dados ambientais utilizando ESP32 e sensores de baixo custo  
- Realizar a comunicação dos dados via protocolo MQTT  
- Armazenar e organizar os dados em banco NoSQL (MongoDB)  
- Desenvolver fluxos de processamento e visualização no Node-RED  
- Aplicar inteligência artificial híbrida para detecção de anomalias  
- Disponibilizar dashboards web para acompanhamento em tempo real e histórico  

---

## 🧠 Arquitetura do Sistema

O sistema foi estruturado em camadas, conforme arquitetura IoT clássica:

1. **Camada de Sensoriamento**  
   - ESP32  
   - Sensores:
     - DHT22 (temperatura e umidade do ar)
     - BH1750 (luminosidade)
     - HD-38 (umidade do solo)

2. **Camada de Comunicação**  
   - Protocolo MQTT (Mosquitto)
   - Publicação de telemetria e status do dispositivo

3. **Camada de Processamento e Persistência**  
   - Servidor local virtualizado com Proxmox
   - Node-RED para lógica, integração e dashboards
   - MongoDB para armazenamento de séries temporais e perfis de cultivo

4. **Camada de Inteligência Artificial**  
   - Sistema especialista baseado em regras agronômicas
   - Modelo não supervisionado Isolation Forest para detecção de padrões anômalos
   - Camada de explicabilidade (XAI) baseada em estatísticas horárias

---

## 🤖 Inteligência Artificial Híbrida

A abordagem adotada combina duas estratégias complementares:

### 🔹 Sistema Especialista
- Baseado em regras agronômicas
- Considera limites ideais por perfil de cultivo
- Avalia contexto temporal (dia/noite)
- Gera alertas determinísticos e interpretáveis

### 🔹 Isolation Forest
- Algoritmo não supervisionado
- Treinado com grande volume de dados reais
- Detecta padrões estatisticamente raros
- Reduz falsos positivos
- Atua apenas quando há comportamento atípico multivariado

### 🔹 XAI (Explainable AI)
- Utiliza médias e desvios padrão por hora do dia
- Identifica qual variável mais contribuiu para o desvio
- Fornece explicações textuais ao usuário final

---

## 📊 Visualização e Interface

O sistema disponibiliza dashboards web desenvolvidos no Node-RED, permitindo:
- Visualização em tempo real
- Análise histórica dos sensores
- Exibição de alertas e recomendações da IA
- Gerenciamento de perfis de cultivo

---

## 📂 Estrutura do Repositório

# Monitoramento Inteligente em Orquidário de Pequenos Cultivadores

Este repositório reúne os códigos-fonte, fluxos, scripts e materiais complementares desenvolvidos no Trabalho de Conclusão de Curso (TCC) intitulado **“Monitoramento Inteligente em Orquidário de Pequenos Cultivadores”**, apresentado ao **Instituto Federal de São Paulo (IFSP)**, no curso de **Pós-Graduação em Internet das Coisas (IoT)**.

O projeto propõe uma solução de monitoramento ambiental inteligente voltada a pequenos produtores de orquídeas, integrando **Internet das Coisas (IoT)**, **processamento em servidor local**, **inteligência artificial híbrida** e **análise estatística**, com foco em baixo custo, explicabilidade e aplicabilidade prática.

---

## 📌 Contexto e Motivação

O cultivo de orquídeas é altamente sensível a variações ambientais, como temperatura, umidade do ar, umidade do solo e luminosidade. Pequenos produtores, em geral, não dispõem de ferramentas tecnológicas acessíveis que permitam o acompanhamento contínuo dessas variáveis, o que pode resultar em estresse fisiológico das plantas, doenças e perdas produtivas.

Nesse contexto, este trabalho busca oferecer uma alternativa tecnológica acessível, baseada em sensores IoT e análise inteligente dos dados coletados, permitindo:
- Monitoramento contínuo (24/7)
- Registro histórico confiável
- Detecção de desvios ambientais
- Apoio à tomada de decisão do produtor

---

## 🎯 Objetivo Geral

Desenvolver um sistema inteligente de monitoramento ambiental para orquidários, integrando sensores IoT, comunicação MQTT, processamento em servidor local e inteligência artificial híbrida, visando auxiliar pequenos cultivadores na gestão das condições ambientais.

---

## 🎯 Objetivos Específicos

- Implementar a coleta de dados ambientais utilizando ESP32 e sensores de baixo custo  
- Realizar a comunicação dos dados via protocolo MQTT  
- Armazenar e organizar os dados em banco NoSQL (MongoDB)  
- Desenvolver fluxos de processamento e visualização no Node-RED  
- Aplicar inteligência artificial híbrida para detecção de anomalias  
- Disponibilizar dashboards web para acompanhamento em tempo real e histórico  

---

## 🧠 Arquitetura do Sistema

O sistema foi estruturado em camadas, conforme arquitetura IoT clássica:

1. **Camada de Sensoriamento**  
   - ESP32  
   - Sensores:
     - DHT22 (temperatura e umidade do ar)
     - BH1750 (luminosidade)
     - HD-38 (umidade do solo – calibrado)

2. **Camada de Comunicação**  
   - Protocolo MQTT (Mosquitto)
   - Publicação de telemetria e status do dispositivo

3. **Camada de Processamento e Persistência**  
   - Servidor local virtualizado com Proxmox
   - Node-RED para lógica, integração e dashboards
   - MongoDB para armazenamento de séries temporais e perfis de cultivo

4. **Camada de Inteligência Artificial**  
   - Sistema especialista baseado em regras agronômicas
   - Modelo não supervisionado Isolation Forest para detecção de padrões anômalos
   - Camada de explicabilidade (XAI) baseada em estatísticas horárias

---

## 🤖 Inteligência Artificial Híbrida

A abordagem adotada combina duas estratégias complementares:

### 🔹 Sistema Especialista
- Baseado em regras agronômicas
- Considera limites ideais por perfil de cultivo
- Avalia contexto temporal (dia/noite)
- Gera alertas determinísticos e interpretáveis

### 🔹 Isolation Forest
- Algoritmo não supervisionado
- Treinado com grande volume de dados reais
- Detecta padrões estatisticamente raros
- Reduz falsos positivos
- Atua apenas quando há comportamento atípico multivariado

### 🔹 XAI (Explainable AI)
- Utiliza médias e desvios padrão por hora do dia
- Identifica qual variável mais contribuiu para o desvio
- Fornece explicações textuais ao usuário final

---

## 📊 Visualização e Interface

O sistema disponibiliza dashboards web desenvolvidos no Node-RED, permitindo:
- Visualização em tempo real
- Análise histórica dos sensores
- Exibição de alertas e recomendações da IA
- Gerenciamento de perfis de cultivo

---

## 📂 Estrutura do Repositório

/esp32 → Código-fonte do firmware do ESP32
/node-red → Fluxos do Node-RED
/ia → Scripts Python da Inteligência Artificial
/docs → Documentação complemental


---

## 🛠️ Tecnologias Utilizadas

- ESP32
- MQTT (Mosquitto)
- Node-RED
- MongoDB
- Python
- Scikit-learn
- Isolation Forest
- Docker / Proxmox
- Dashboards Web

---

## ⚠️ Limitações Identificadas

- Uso de apenas um nó sensor
- IA voltada à detecção, não à predição
- Ausência de automação ativa (atuadores)

---

## 🔮 Trabalhos Futuros

- Implementação de rede mesh de sensores
- Modelos preditivos baseados em LSTM
- Automação ativa do ambiente
- Integração com visão computacional
- Expansão para outros tipos de cultivo


## 📄 Referência Acadêmica

Este repositório está vinculado ao Trabalho de Conclusão de Curso apresentado em 2025, como parte dos requisitos para obtenção do título de especialista em Internet das Coisas.
