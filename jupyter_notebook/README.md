# Jupyter Notebooks – Treinamento e Validação da Inteligência Artificial

Esta pasta contém os notebooks Jupyter utilizados nas etapas de **treinamento**, **validação** e **análise experimental** do modelo de Inteligência Artificial desenvolvido no projeto de monitoramento inteligente do orquidário.

Os notebooks foram empregados como ambiente exploratório e experimental, permitindo análise detalhada dos dados, ajustes de parâmetros e avaliação do comportamento do modelo antes de sua implementação final no sistema em produção.

---

## 📂 Notebooks Disponíveis

### 📘 Treino_Final_IA.ipynb

Este notebook é responsável pela **etapa de treinamento do modelo de detecção de anomalias**, utilizando dados reais coletados pelos sensores IoT do sistema.

#### Principais atividades realizadas:
- Importação dos dados provenientes do banco MongoDB
- Limpeza e pré-processamento das leituras dos sensores
- Normalização das variáveis ambientais
- Seleção das *features* utilizadas pelo modelo
- Treinamento do algoritmo **Isolation Forest** (modelo não supervisionado)
- Ajuste de hiperparâmetros
- Geração do modelo treinado (`.pkl`)
- Análise exploratória dos padrões ambientais

Este processo foi conduzido com base em **dados reais**, captados continuamente por sensores instalados em um orquidário experimental, totalizando **126.765 registros**.

---

### 📗 Validacao_Final_TCC.ipynb

Este notebook contempla a **etapa de validação experimental do modelo**, com foco na análise de desempenho e interpretação dos resultados.

#### Principais atividades realizadas:
- Criação de rótulos de referência (*ground truth*) a partir de regras agronômicas
- Avaliação do modelo treinado em dados não vistos
- Construção da matriz de confusão
- Cálculo das métricas de desempenho:
  - Acurácia
  - Precisão
  - Recall
  - F1-score
- Análise do comportamento do modelo frente a dados extremos
- Discussão sobre generalização, robustez e ausência de *overfitting*

A validação foi realizada de forma comparativa, confrontando as decisões do modelo estatístico com o sistema especialista baseado em regras.

---

## 🧠 Abordagem Metodológica

A Inteligência Artificial adotada neste projeto segue uma abordagem **híbrida**, composta por:

- **Sistema Especialista**: regras agronômicas determinísticas
- **Modelo Estatístico Não Supervisionado**: Isolation Forest
- **Camada de Explicabilidade (XAI)**: baseada em estatísticas horárias (média e desvio padrão)

Os notebooks representam a fase experimental que fundamenta a implementação final do script `ia_main.py`, responsável pela execução em tempo real.

---

## ⚠️ Observações Importantes

- Os notebooks não devem ser utilizados diretamente em produção.
- As credenciais de acesso a banco de dados e serviços externos não estão incluídas.
- Os dados utilizados são reais, porém não estão disponibilizados integralmente neste repositório por questões de volume e privacidade.

---

## 🎓 Contexto Acadêmico

Estes notebooks fazem parte do Trabalho de Conclusão de Curso (TCC) intitulado **“Monitoramento Inteligente em Orquidário de Pequenos Cultivadores”**, apresentado ao Instituto Federal de São Paulo (IFSP), no curso de Pós-Graduação em Internet das Coisas (IoT).

Eles documentam o processo científico de experimentação, análise e validação que embasa a solução proposta.

