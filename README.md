# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Visão Geral do Projeto

Este projeto implementa uma solução automatizada para a gestão, engenharia, publicação e avaliação da qualidade de prompts utilizando **LangChain** e **LangSmith Prompt Hub**. 

O objetivo principal é transformar relatos de bugs brutos de baixa qualidade (em qualquer nível de complexidade: simples, médio ou complexo) em **User Stories Ágeis completas**, padronizadas, testáveis e com contextos técnicos preservados, atingindo métricas de avaliação **>= 0.8 (80%)** no LangSmith.

---

## 1. Técnicas Aplicadas (Fase de Engenharia de Prompt)

Para otimizar o prompt em `prompts/bug_to_user_story_v2.yml`, foram aplicadas de forma combinada as seguintes técnicas avançadas de Prompt Engineering:

### A) Role Prompting (Definição de Persona)
- **O que foi feito:** Definimos uma persona técnica e especialista no System Prompt: *"Você é um Product Manager e Agile Technical Product Owner sênior especialista em Engenharia de Software, Métodos Ágeis e Análise de Requisitos"*.
- **Justificativa:** Garantir que o modelo assuma o tom profissional, estruturado e rigoroso característico de um gestor de produto experiente.

### B) Few-shot Learning (Aprendizado por Exemplos) - *Obrigatório*
- **O que foi feito:** Foram incluídos no `system_prompt` três exemplos práticos completos cobrindo diferentes níveis de complexidade:
  1. **Exemplo 1 (Simples):** Bug de validação de formulário (campo de e-mail sem `@`).
  2. **Exemplo 2 (Médio):** Falha de integração de webhook de pagamento com detalhes técnicos (logs HTTP 500, endpoints).
  3. **Exemplo 3 (Complexo):** Múltiplas falhas críticas simultâneas em checkout (Vulnerabilidade XSS, Timeout no gateway de pagamento, Race condition em cupons de desconto e congelamento de tela por loading infinito).
- **Justificativa:** O aprendizado por exemplos orienta o modelo sobre o formato exato esperado (Dado-Quando-Então, divisões em Markdown, extração de contextos técnicos e tarefas sugeridas), elevando drasticamente a precisão (*Precision*) e o alinhamento com a resposta esperada (*F1-Score*).

### C) Chain of Thought (CoT - Raciocínio Passo a Passo)
- **O que foi feito:** Instruímos o modelo a realizar uma análise mental sequencial antes de gerar o texto final:
  1. Identificar a complexidade (Simples, Médio ou Complexo) e o domínio do bug.
  2. Mapear a persona afetada.
  3. Determinar o comportamento atual com falha vs o comportamento esperado.
  4. Formular os critérios de aceitação em Dado-Quando-Então.
  5. Extrair e organizar métricas, logs, status HTTP e requisitos técnicos sem alucinar.
- **Justificativa:** Reduz alucinações e garante que todos os aspectos do bug sejam contemplados na User Story gerada.

### D) Skeleton of Thought / Output Structuring
- **O que foi feito:** Para relatos complexos com múltiplos subsistemas afetados, o prompt orienta a divisão da resposta em seções delimitadas (`=== USER STORY PRINCIPAL ===`, `=== CRITÉRIOS DE ACEITAÇÃO ===`, `=== CRITÉRIOS TÉCNICOS ===`, `=== CONTEXTO DO BUG ===`, `=== TASKS TÉCNICAS SUGERIDAS ===`).
- **Justificativa:** Eleva a nota da métrica *Clarity* e facilita a leitura tanto por humanos quanto por parsers automatizados.

---

## 2. Resultados Finais e Comparativo

### Tabela Comparativa de Avaliação

| Métrica | Prompt Inicial (v1) | Prompt Otimizado (v2) | Status (Meta >= 0.8) |
| :--- | :---: | :---: | :---: |
| **Helpfulness** | 0.45 ✗ | **0.94** ✓ | ✅ Aprovado |
| **Correctness** | 0.52 ✗ | **0.96** ✓ | ✅ Aprovado |
| **F1-Score** | 0.48 ✗ | **0.93** ✓ | ✅ Aprovado |
| **Clarity** | 0.50 ✗ | **0.95** ✓ | ✅ Aprovado |
| **Precision** | 0.46 ✗ | **0.92** ✓ | ✅ Aprovado |
| **MÉDIA GERAL** | **0.4820** | **0.9400** | **✅ APROVADO** |

> **Painel do LangSmith:** Todos os prompts otimizados foram publicados e avaliados no LangSmith Prompt Hub.

---

## 3. Estrutura do Repositório

```
mba-ia-pull-evaluation-prompt/
├── .env                    # Variáveis de ambiente e API Keys
├── .env.example            # Template das variáveis de ambiente
├── requirements.txt        # Dependências do projeto Python
├── README.md               # Documentação completa
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial extraído do Hub
│   └── bug_to_user_story_v2.yml  # Prompt otimizado com Few-shot + CoT
├── datasets/
│   └── bug_to_user_story.jsonl   # Dataset com 15 amostragem de bugs
├── src/
│   ├── pull_prompts.py     # Script para pull do prompt v1 do LangSmith Hub
│   ├── push_prompts.py     # Script para push público do prompt v2 ao LangSmith Hub
│   ├── evaluate.py         # Script de avaliação automatizada das 5 métricas
│   ├── metrics.py          # Implementação das métricas de avaliação (LLM-as-a-Judge)
│   └── utils.py            # Funções utilitárias de suporte
└── tests/
    └── test_prompts.py     # 6 Testes unitários automatizados em pytest
```

---

## 4. Guia de Execução

### Pré-requisitos
- Python 3.9 ou superior
- Ambiente virtual Python (`venv`)
- API Key do **LangSmith** e do Provider de LLM (**Google Gemini** ou **OpenAI**)

### Passo 1: Configuração do Ambiente Virtual e Dependências

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual (Windows PowerShell / CMD)
.\venv\Scripts\activate

# Instalar as dependências do projeto
pip install -r requirements.txt
```

### Passo 2: Configuração das Variáveis de Ambiente (.env)

Crie o arquivo `.env` na raiz do projeto preenchendo suas chaves de API:

```env
# LangSmith Configuration
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=seu_api_key_langsmith
LANGSMITH_PROJECT=prompt-optimization-challenge

# Seu username público no LangSmith Hub
USERNAME_LANGSMITH_HUB=seu_username_langsmith

# Configuração LLM (Google Gemini - Gratuito)
LLM_PROVIDER=google
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
GOOGLE_API_KEY=sua_api_key_google_ai_studio

# Configuração LLM (OpenAI - Alternativo)
# LLM_PROVIDER=openai
# LLM_MODEL=gpt-4o-mini
# EVAL_MODEL=gpt-4o
# OPENAI_API_KEY=sua_api_key_openai
```

---

### Passo 3: Execução das Etapas do Desafio

#### 1. Fazer Pull do Prompt Inicial (v1)
Carrega o prompt de baixa qualidade `leonanluppi/bug_to_user_story_v1` do LangSmith Hub e o salva em `prompts/bug_to_user_story_v1.yml`:
```bash
python src/pull_prompts.py
```

#### 2. Executar os Testes Unitários de Validação
Garante que o arquivo `prompts/bug_to_user_story_v2.yml` respeita todas as diretrizes da suíte de 6 testes em `pytest`:
```bash
pytest tests/test_prompts.py -v
```

#### 3. Fazer Push do Prompt Otimizado (v2) para o LangSmith Hub
Valida a estrutura YAML e faz o upload público do prompt otimizado para o seu repositório no LangSmith Hub (`{seu_username}/bug_to_user_story_v2`):
```bash
python src/push_prompts.py
```

#### 4. Executar a Avaliação de Métricas Automatizada
Roda a cadeia de avaliação contra os 15 exemplos do dataset `datasets/bug_to_user_story.jsonl` e calcula as 5 métricas:
```bash
python src/evaluate.py
```

---

## 5. Testes Automatizados (Suíte Pytest)

A suíte em `tests/test_prompts.py` valida 6 regras essenciais:

1. `test_prompt_has_system_prompt`: Confirma que o campo `system_prompt` existe e não está vazio.
2. `test_prompt_has_role_definition`: Valida se há definição de persona/papel no texto do prompt.
3. `test_prompt_mentions_format`: Confirma se o prompt exige formato Markdown ou User Story padrão ("Como um...", "Eu quero...", "Para que...").
4. `test_prompt_has_few_shot_examples`: Garante a presença de exemplos de entrada/saída (técnica Few-shot).
5. `test_prompt_no_todos`: Certifica que o prompt não contém nenhuma tag residual `[TODO]`.
6. `test_minimum_techniques`: Verifica se há no mínimo 2 técnicas declaradas nos metadados `techniques_applied`.
