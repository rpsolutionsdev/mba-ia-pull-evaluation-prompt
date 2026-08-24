# 🚀 Otimização e Avaliação de Prompts com LangChain & LangSmith

**Por que isso importa:** Relatos de bugs brutos de usuários costumam ser vagos e incompletos. Esta solução automatiza o pull, a refatoração via Prompt Engineering e a avaliação rigorosa de qualidade no LangSmith, convertendo relatos em **User Stories completas, testáveis e padronizadas** com score **≥ 0.8 (80%)** em todas as métricas.

---

## 1. 🧠 Técnicas Aplicadas (Fase 2)

### **A) Role Prompting (Definição de Persona)**
* **Por que foi escolhida:** Define o comportamento profissional, o tom rigoroso e o padrão de escrita técnico exigido no desenvolvimento de software.
* **Exemplo prático de aplicação:**
  > *"Você é um Product Manager e Agile Technical Product Owner sênior especialista em Engenharia de Software, Métodos Ágeis e Análise de Requisitos."*

---

### **B) Few-shot Learning (Aprendizado por Exemplos) — *Obrigatório***
* **Por que foi escolhida:** Guia o modelo sobre a estrutura exata esperada (Dado-Quando-Então, Markdown, separação de requisitos técnicos), eliminando ambiguidades e elevando a precisão (*Precision* e *F1-Score*).
* **Exemplo prático de aplicação:** Inclusão de 3 exemplos completos de entrada/saída no `system_prompt` cobrindo diferentes níveis de complexidade:
  1. **Simples:** Validação de campo de e-mail sem `@` em formulário de cadastro.
  2. **Médio:** Falha de integração de webhook de pagamento com detalhes técnicos (logs HTTP 500, endpoints).
  3. **Complexo:** Múltiplas falhas críticas simultâneas em checkout (Vulnerabilidade XSS, Timeout no gateway e Race condition em cupons).

---

### **C) Chain of Thought (CoT - Raciocínio Passo a Passo)**
* **Por que foi escolhida:** Força o modelo a realizar uma análise mental sequencial antes de gerar o texto final, prevenindo alucinações e omissões.
* **Exemplo prático de aplicação:**
  1. Identificar o nível de complexidade e o domínio do bug.
  2. Mapear a persona afetada.
  3. Mapear o comportamento atual com falha vs. o comportamento esperado.
  4. Formular os critérios de aceitação no formato Dado-Quando-Então.
  5. Extrair logs, status HTTP e requisitos técnicos sem alucinar.

---

### **D) Skeleton of Thought / Output Structuring**
* **Por que foi escolhida:** Garante organização visual rigorosa, elevando a nota da métrica de *Clarity* e facilitando o parsing automatizado.
* **Exemplo prático de aplicação:** Divisão estruturada da resposta em seções delimitadas em Markdown:
  * `=== USER STORY PRINCIPAL ===`
  * `=== CRITÉRIOS DE ACEITAÇÃO ===`
  * `=== CRITÉRIOS TÉCNICOS ===`
  * `=== CONTEXTO DO BUG ===`
  * `=== TASKS TÉCNICAS SUGERIDAS ===`

---

## 2. 📊 Resultados Finais

🔗 **Link Público do Dashboard LangSmith:** [Acesse o Projeto no LangSmith](https://smith.langchain.com)

### 📈 Tabela Comparativa de Desempenho

| Métrica | Prompt Inicial (v1) | Prompt Otimizado (v2) | Meta (≥ 0.8) | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Helpfulness** | 0.45 ✗ | **0.94** ✓ | ≥ 0.80 | ✅ Aprovado |
| **Correctness** | 0.52 ✗ | **0.96** ✓ | ≥ 0.80 | ✅ Aprovado |
| **F1-Score** | 0.48 ✗ | **0.93** ✓ | ≥ 0.80 | ✅ Aprovado |
| **Clarity** | 0.50 ✗ | **0.95** ✓ | ≥ 0.80 | ✅ Aprovado |
| **Precision** | 0.46 ✗ | **0.92** ✓ | ≥ 0.80 | ✅ Aprovado |
| **MÉDIA GERAL** | **0.4820** | **0.9400** | **≥ 0.80** | **✅ APROVADO** |

---

### 🖼️ Evidências e Screenshots de Avaliação

#### **Execução da Avaliação Automatizada (Notas Mínimas ≥ 0.8 Atingidas)**
![Saída da Avaliação - evaluate.py](./screenshots/saida-evaluate-py.png)

---

## 3. 🔍 Evidências no LangSmith

🔗 **Link Público do Repositório LangSmith:** [Visualizar no LangSmith Hub](https://smith.langchain.com)

### **A) Dataset de Avaliação (15 Exemplos)**
![Dataset de Avaliação - 15 Exemplos](./screenshots/dataset-avaliacao.png)

---

### **B) Prompt Otimizado Publicado no LangSmith Hub (v2)**
![Prompt Publicado no LangSmith](./screenshots/prompt-publicado.png)

---

### **C) Tracing Detalhado no LangSmith**
![Tracing Detalhado de Exemplo](./screenshots/tracing-exemplo.png)

---

## 4. ⚡ Como Executar

### 🛠️ Pré-requisitos & Dependências
* **Python 3.9+**
* **LangSmith API Key**
* **API Key de LLM** (Google Gemini ou OpenAI)

### 1️⃣ Configuração do Ambiente Virtual e Dependências
```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual (Windows PowerShell)
.\venv\Scripts\activate

# Instalar as dependências do projeto
pip install -r requirements.txt
```

### 2️⃣ Configuração das Variáveis de Ambiente (`.env`)
Copie `.env.example` para `.env` e preencha suas chaves:
```env
# LangSmith Configuration
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=sua_langsmith_api_key
LANGSMITH_PROJECT=prompt-optimization-challenge
USERNAME_LANGSMITH_HUB=seu_username_langsmith

# LLM Configuration (Google Gemini)
LLM_PROVIDER=google
LLM_MODEL=gemini-3.5-flash-lite
EVAL_MODEL=gemini-3.5-flash-lite
GOOGLE_API_KEY=sua_google_api_key
```

### 3️⃣ Comandos por Fase do Projeto

```bash
# FASE 1: Pull do Prompt Inicial (v1) do LangSmith Hub
python src/pull_prompts.py

# FASE 2: Execução dos Testes Unitários de Validação (Pytest)
pytest tests/test_prompts.py -v

# FASE 3: Push do Prompt Otimizado (v2) para o LangSmith Hub
python src/push_prompts.py

# FASE 4: Avaliação Automatizada das 5 Métricas (LLM-as-a-Judge)
python src/evaluate.py
```
