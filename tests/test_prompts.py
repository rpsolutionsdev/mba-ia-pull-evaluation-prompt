"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Carrega as configurações do prompt v2 antes de cada teste."""
        v2_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
        assert v2_path.exists(), f"Arquivo não encontrado: {v2_path}"

        self.data = load_prompts(str(v2_path))
        assert "bug_to_user_story_v2" in self.data, "Chave 'bug_to_user_story_v2' não encontrada no YAML"
        self.prompt_config = self.data["bug_to_user_story_v2"]

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt_config, "Campo 'system_prompt' ausente no prompt"
        system_prompt = self.prompt_config["system_prompt"]
        assert isinstance(system_prompt, str), "system_prompt deve ser uma string"
        assert len(system_prompt.strip()) > 0, "system_prompt está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = self.prompt_config.get("system_prompt", "")
        role_keywords = ["você é um", "você é uma", "product manager", "product owner", "persona", "papel"]
        found = any(kw in system_prompt.lower() for kw in role_keywords)
        assert found, "Definição de persona/papel não encontrada no system_prompt"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = self.prompt_config.get("system_prompt", "")
        format_keywords = ["markdown", "como um", "eu quero", "para que", "critérios de aceitação", "user story"]
        found = any(kw in system_prompt.lower() for kw in format_keywords)
        assert found, "Formato de User Story ou Markdown não exigido/mencionado no system_prompt"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = self.prompt_config.get("system_prompt", "")
        example_keywords = ["exemplo", "few-shot", "exemplo 1", "relato de bug:", "user story gerada:"]
        found = any(kw in system_prompt.lower() for kw in example_keywords)
        assert found, "Exemplos Few-shot de entrada/saída não encontrados no system_prompt"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = self.prompt_config.get("system_prompt", "")
        user_prompt = self.prompt_config.get("user_prompt", "")
        assert "[TODO]" not in system_prompt, "system_prompt contém [TODO]"
        assert "[TODO]" not in user_prompt, "user_prompt contém [TODO]"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt_config.get("techniques_applied", [])
        assert isinstance(techniques, list), "techniques_applied deve ser uma lista"
        assert len(techniques) >= 2, f"Pelo menos 2 técnicas devem ser listadas, encontradas: {len(techniques)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])