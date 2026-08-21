"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

# Garantir UTF-8 no stdout/stderr no Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt.

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub.

    Args:
        prompt_name: Nome do prompt (ex: bug_to_user_story_v2)
        prompt_data: Dados do prompt do YAML

    Returns:
        True se sucesso, False caso contrário
    """
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    if not username:
        print("[ERRO] USERNAME_LANGSMITH_HUB não configurada no .env")
        return False

    hub_prompt_handle = f"{username}/{prompt_name}"

    system_prompt = prompt_data.get("system_prompt", "")
    user_prompt = prompt_data.get("user_prompt", "{bug_report}")

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt)
    ])

    description = prompt_data.get("description", "Prompt v2 otimizado para converter relatos de bugs em User Stories")
    tags = prompt_data.get("tags", ["bug-analysis", "user-story"])

    print(f"Fazendo push do prompt para LangSmith Hub: '{hub_prompt_handle}'...")

    # Tentativa 1: Push público com o handle completo {username}/{prompt_name}
    try:
        url = hub.push(
            hub_prompt_handle,
            prompt_template,
            new_repo_is_public=True,
            new_repo_description=description,
            tags=tags
        )
        print(f"[OK] Push realizado com sucesso!")
        print(f"   Handle do Hub: {hub_prompt_handle}")
        print(f"   URL/Ref: {url}")
        return True
    except Exception as e:
        error_msg = str(e)
        if "Nothing to commit" in error_msg:
            print(f"[OK] O prompt já está atualizado no LangSmith Hub (sem alterações).")
            print(f"   Handle do Hub: {hub_prompt_handle}")
            return True

        # Tentativa 2: Push no workspace do usuário
        print(f"   Tentando push no seu workspace no LangSmith...")
        try:
            url = hub.push(
                prompt_name,
                prompt_template,
                new_repo_description=description,
                tags=tags
            )
            print(f"[OK] Push realizado com sucesso no seu workspace!")
            print(f"   URL/Ref: {url}")
            return True
        except Exception as e2:
            error_msg2 = str(e2)
            if "Nothing to commit" in error_msg2:
                print(f"[OK] O prompt já está publicado e atualizado no seu workspace no LangSmith!")
                return True

            print(f"[ERRO] Falha ao fazer push para o LangSmith Hub: {e}")

            if "LangChain Hub handle" in error_msg:
                print("\n" + "=" * 70)
                print("⚠️  AÇÃO NECESSÁRIA NO LANGSMITH:")
                print("=" * 70)
                print("O LangSmith exige a ativação inicial do seu Handle público antes do primeiro push.\n")
                print("Siga os passos abaixo (leva menos de 1 minuto):")
                print("1. Acesse: https://smith.langchain.com/prompts")
                print("2. Clique no botão '+' (New Prompt) no canto superior direito.")
                print(f"3. Confirme seu handle como '{username}' e salve qualquer prompt inicial de teste.")
                print("\nApós salvar uma vez no site, rode novamente: python src/push_prompts.py")
                print("=" * 70 + "\n")
            return False


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS AO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    v2_path = "prompts/bug_to_user_story_v2.yml"
    print(f"Carregando prompt otimizado de '{v2_path}'...")

    yaml_data = load_yaml(v2_path)
    if not yaml_data:
        print(f"[ERRO] Não foi possível carregar o arquivo '{v2_path}'")
        return 1

    prompt_key = "bug_to_user_story_v2"
    if prompt_key not in yaml_data:
        print(f"[ERRO] Chave '{prompt_key}' não encontrada no arquivo '{v2_path}'")
        return 1

    prompt_data = yaml_data[prompt_key]

    print("Validando estrutura do prompt...")
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("[ERRO] Validação do prompt falhou:")
        for err in errors:
            print(f"   - {err}")
        return 1

    print("[OK] Prompt validado com sucesso!")

    success = push_prompt_to_langsmith(prompt_key, prompt_data)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
