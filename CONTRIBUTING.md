# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o projeto! Este documento contém diretrizes para contribuições.

## Como Contribuir

### 1. Reportar Bugs 🐛

Antes de reportar, verifique:
- [ ] Já executou `python test_setup.py`?
- [ ] Já consultou o `FAQ.md`?
- [ ] Já procurou em issues existentes?

Se sim, crie uma issue com:
- **Descrição clara** do problema
- **Passos para reproduzir**
- **Comportamento esperado vs real**
- **Logs completos** (copie do terminal)
- **Ambiente**: SO, versão Python, provedor LLM
- **Configuração**: (sem expor API keys!)

### 2. Sugerir Funcionalidades 💡

Crie uma issue descrevendo:
- **Problema que resolve**: Por que essa feature é útil?
- **Solução proposta**: Como deveria funcionar?
- **Alternativas consideradas**: Outras opções?
- **Contexto adicional**: Screenshots, exemplos, etc.

### 3. Contribuir com Código 💻

#### Preparação

```bash
# Fork o repositório e clone
git clone https://github.com/seu-usuario/99LANGCORE.git
cd 99LANGCORE

# Instale dependências de desenvolvimento
pip install -r requirements.txt
pip install black flake8 mypy pytest

# Crie um branch
git checkout -b feature/minha-feature
```

#### Padrões de Código

**Python Style Guide**: PEP 8

```bash
# Formatar código
black .

# Verificar estilo
flake8 .

# Type checking
mypy *.py
```

**Convenções**:
- ✅ Use type hints
- ✅ Docstrings em funções públicas
- ✅ Nomes descritivos (inglês ou português, seja consistente)
- ✅ Máximo 88 caracteres por linha (Black default)
- ✅ Imports organizados: stdlib → third-party → local

**Exemplo**:

```python
from typing import List, Optional
import logging

def processar_pedido(order_id: str, retry: bool = True) -> Optional[dict]:
    """
    Processa um pedido específico e retorna o resultado.
    
    Args:
        order_id: ID do pedido no formato string
        retry: Se True, tenta novamente em caso de falha
    
    Returns:
        Dict com resultado ou None se falhar
    
    Raises:
        ValueError: Se order_id for inválido
    """
    if not order_id:
        raise ValueError("order_id não pode ser vazio")
    
    # Lógica aqui...
    return {"status": "success"}
```

#### Testes

```bash
# Executar testes
pytest

# Com cobertura
pytest --cov=. --cov-report=html
```

**Crie testes para**:
- Novas funcionalidades
- Correções de bugs
- Edge cases

**Exemplo de teste**:

```python
# test_api_client.py
import pytest
from api_client import APIClient

def test_get_order_detail_success():
    client = APIClient("http://localhost:3002")
    result = client.get_order_detail("123456")
    assert result["success"] is True
    assert "data" in result

def test_get_order_detail_invalid_id():
    client = APIClient("http://localhost:3002")
    with pytest.raises(ValueError):
        client.get_order_detail("")
```

#### Commit Messages

Formato: `tipo: descrição curta`

**Tipos**:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudanças na documentação
- `style`: Formatação (sem mudança de código)
- `refactor`: Refatoração
- `test`: Adicionar/modificar testes
- `chore`: Tarefas de manutenção

**Exemplos**:

```bash
git commit -m "feat: adiciona suporte a Claude AI"
git commit -m "fix: corrige timeout em requests lentos"
git commit -m "docs: atualiza FAQ com novos erros comuns"
git commit -m "refactor: simplifica lógica do grafo LangGraph"
```

#### Pull Request

```bash
# Antes de enviar
black .
flake8 .
pytest
python test_setup.py

# Push
git push origin feature/minha-feature
```

**No PR, inclua**:
- Descrição clara das mudanças
- Por que essa mudança é necessária
- Como foi testado
- Screenshots (se UI/logs)
- Issues relacionadas (ex: "Closes #123")

### 4. Melhorar Documentação 📖

Documentação é tão importante quanto código!

**Você pode**:
- Corrigir erros de português/inglês
- Adicionar exemplos
- Melhorar explicações
- Traduzir para outros idiomas
- Adicionar diagramas/ilustrações

**Arquivos de documentação**:
- `README.pt-BR.md`
- `GUIA_INSTALACAO.md`
- `FAQ.md`
- `ARQUITETURA.md`
- `DEPLOYMENT.md`

## Áreas que Precisam de Ajuda

### Prioridade Alta 🔴

- [ ] Testes unitários (cobertura < 50%)
- [ ] Processamento paralelo (asyncio)
- [ ] Retry logic robusto
- [ ] Validação de inputs

### Prioridade Média 🟡

- [ ] Suporte a Claude (Anthropic)
- [ ] Dashboard web
- [ ] Cache de respostas
- [ ] Notificações (Telegram, Email)

### Prioridade Baixa 🟢

- [ ] Interface gráfica
- [ ] Suporte a outros idiomas
- [ ] Análise de sentimento
- [ ] Exportação de relatórios

## Estrutura do Projeto

```
99LANGCORE/
├── main.py              # Entry point
├── config.py            # Configurações
├── models.py            # Schemas Pydantic
├── api_client.py        # Cliente HTTP
├── llm_client.py        # Factory LLM
├── agent_graph.py       # Grafo LangGraph
├── tests/               # (TODO: criar)
│   ├── test_api.py
│   ├── test_llm.py
│   └── test_graph.py
└── docs/                # Documentação
```

## Checklist Antes de Submeter PR

- [ ] Código segue PEP 8
- [ ] Passou no `black .`
- [ ] Passou no `flake8 .`
- [ ] Adicionou testes (se aplicável)
- [ ] Testes passando (`pytest`)
- [ ] Atualizou documentação
- [ ] Atualizou `CHANGELOG.md`
- [ ] Testou manualmente (`python main.py`)
- [ ] Commit messages seguem padrão

## Processo de Review

1. **Automático**: CI/CD roda testes e linters
2. **Manual**: Maintainer revisa código
3. **Feedback**: Discussão e ajustes
4. **Merge**: Após aprovação

**Tempo médio**: 3-7 dias

## Código de Conduta

### Nossos Valores

- 🤝 Respeito e inclusão
- 🌟 Colaboração construtiva
- 📚 Compartilhamento de conhecimento
- 🎯 Foco na qualidade

### Comportamentos Esperados

- ✅ Seja gentil e respeitoso
- ✅ Aceite feedback construtivo
- ✅ Foque no que é melhor para a comunidade
- ✅ Mostre empatia com outros

### Comportamentos Inaceitáveis

- ❌ Assédio ou discriminação
- ❌ Comentários ofensivos
- ❌ Ataques pessoais
- ❌ Spam ou trolling

## Perguntas?

- **Bug ou feature?** → Crie uma issue
- **Dúvida de uso?** → Leia `FAQ.md` primeiro
- **Dúvida de código?** → Leia `ARQUITETURA.md`
- **Outra dúvida?** → Abra uma issue com label "question"

## Agradecimentos

Toda contribuição é valiosa, seja:
- Código
- Documentação
- Reportar bugs
- Sugerir melhorias
- Compartilhar o projeto

**Obrigado por fazer este projeto melhor!** 🚀

---

**Recursos Úteis**:
- [PEP 8 - Style Guide](https://pep8.org/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
