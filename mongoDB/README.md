# Dataset MongoDB – Orquidário

Esta pasta documenta o conjunto de dados utilizado no treinamento e validação do modelo de Inteligência Artificial do projeto.

O dataset **não foi obtido a partir de bases públicas**, nem gerado artificialmente.  
Ele foi construído **exclusivamente a partir de dados reais**, coletados continuamente por sensores instalados em um orquidário experimental.

---

## 📌 Origem dos Dados

Os dados foram coletados por meio de um dispositivo **ESP32**, equipado com sensores ambientais, e transmitidos via protocolo MQTT para um servidor local, onde foram armazenados em banco de dados MongoDB.

Cada registro representa uma leitura ambiental captada em tempo real.

---

## 🌱 Sensores Utilizados

- DHT22  
  - Temperatura do ar (°C)  
  - Umidade relativa do ar (%)

- BH1750  
  - Luminosidade (Lux)

- HD-38  
  - Umidade do solo (% – sensor calibrado)

---

## 📊 Volume de Dados

O conjunto de dados utilizado contém:

- **126.765 registros reais**
- Leituras contínuas ao longo de múltiplos dias
- Variação natural de condições ambientais
- Presença de ruídos e transições reais de ambiente

Esse volume contribuiu para o treinamento de um modelo robusto e bem generalizado.

---

## 🧠 Uso do Dataset na Inteligência Artificial

Os dados armazenados no MongoDB foram utilizados para:

- Análise exploratória dos padrões ambientais
- Cálculo de estatísticas horárias de normalidade
- Treinamento de um modelo não supervisionado (Isolation Forest)
- Validação do comportamento da IA em cenários reais

---

## ⚠️ Observações Importantes

- Dados sensíveis e informações pessoais não estão presentes neste dataset.
- As credenciais de acesso ao banco de dados não são disponibilizadas neste repositório.
- Este repositório não contém uma cópia completa do banco de dados, apenas a documentação de sua estrutura e uso.

---

## 🎓 Contexto Acadêmico

Este dataset foi utilizado no Trabalho de Conclusão de Curso (TCC) apresentado ao Instituto Federal de São Paulo (IFSP), no curso de Pós-Graduação em Internet das Coisas (IoT), como base para o desenvolvimento e avaliação da Inteligência Artificial do sistema.
