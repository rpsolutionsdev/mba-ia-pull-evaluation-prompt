"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub (leonanluppi/bug_to_user_story_v1)
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

# Garantir UTF-8 no stdout/stderr no Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()


def pull_prompts_from_langsmith() -> bool:
    """
    Faz pull do prompt do LangSmith Hub e salva localmente em YAML.
    """
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    prompt_handle = "leonanluppi/bug_to_user_story_v1"
    print(f"Fazendo pull do prompt '{prompt_handle}'...")

    try:
        prompt_template = hub.pull(prompt_handle)

        system_prompt = ""
        user_prompt = "{bug_report}"

        for msg in prompt_template.messages:
            if hasattr(msg, 'prompt') and hasattr(msg.prompt, 'template'):
                text = msg.prompt.template
            elif hasattr(msg, 'content'):
                text = str(msg.content)
            else:
                text = str(msg)

            msg_type = type(msg).__name__.lower()
            if "system" in msg_type:
                system_prompt = text
            elif "human" in msg_type or "user" in msg_type:
                user_prompt = text

        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "version": "v1",
                "created_at": "2025-01-15",
                "tags": ["bug-analysis", "user-story", "product-management"]
            }
        }

        output_path = "prompts/bug_to_user_story_v1.yml"
        if save_yaml(prompt_data, output_path):
            print(f"[OK] Prompt salvo com sucesso em '{output_path}'")
            return True
        else:
            print(f"[ERRO] Erro ao salvar prompt em '{output_path}'")
            return False

    except Exception as e:
        print(f"[ERRO] Erro ao fazer pull do prompt: {e}")
        return False


def main():
    """Função principal"""
    success = pull_prompts_from_langsmith()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
