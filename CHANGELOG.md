# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-01-28

### ✨ Adicionado

- Sistema completo de contestação automática via IA
- Suporte a OpenAI (GPT-4o) e Google Gemini
- Análise multimodal (texto + imagem)
- Orquestração com LangGraph
- Cliente HTTP para API 99Food
- Configuração via arquivo `.env`
- Scripts de teste (`test_setup.py`, `test_llm_only.py`)
- Exemplos de uso programático (`example_usage.py`)
- Documentação completa:
  - `README.md` (inglês)
  - `README.pt-BR.md` (português)
  - `GUIA_INSTALACAO.md`
  - `ARQUITETURA.md`
  - `FAQ.md`
  - `DEPLOYMENT.md`
  - `QUICKSTART.md`
- Scripts de instalação automática:
  - `install.sh` (Linux/Mac)
  - `install.ps1` (Windows)
- Suporte a Docker (`Dockerfile`, `docker-compose.yml`)
- Logs detalhados com emojis
- Tratamento robusto de erros
- Factory pattern para provedores LLM
- State machine usando LangGraph
- Modelos Pydantic para tipagem

### 🔒 Segurança

- `.gitignore` configurado para proteger `.env`
- Timeout de 30s para requisições HTTP
- Validação de schemas com Pydantic

### 📝 Documentação

- README completo com exemplos
- FAQ com troubleshooting
- Guia de instalação passo a passo
- Documentação de arquitetura técnica
- Guia de deployment e automação

---

## [Futuro] - Roadmap

### Planejado para v1.1.0

- [ ] Suporte a Claude (Anthropic)
- [ ] Processamento paralelo com `asyncio`
- [ ] Cache de respostas para motivos similares
- [ ] Dashboard web para monitoramento
- [ ] Exportação de relatórios (CSV, Excel)
- [ ] Integração com Telegram para notificações
- [ ] Webhook para receber eventos em tempo real

### Planejado para v1.2.0

- [ ] Machine Learning para melhorar defesas
- [ ] Análise de sentimento das reclamações
- [ ] Geração automática de evidências (screenshots)
- [ ] Multi-idioma (inglês, espanhol)
- [ ] API REST própria
- [ ] Interface gráfica (web UI)

### Considerando para v2.0.0

- [ ] Suporte a múltiplas plataformas (iFood, Rappi)
- [ ] Sistema de regras customizáveis
- [ ] IA treinada especificamente para contestações
- [ ] Análise preditiva (quais contestações terão sucesso)
- [ ] Integração com sistemas de gestão (ERP)

---

## Como Contribuir

Se você implementou alguma dessas funcionalidades ou tem sugestões:

1. Documente a mudança aqui
2. Atualize a versão seguindo [Semantic Versioning](https://semver.org/)
3. Atualize os arquivos relevantes (README, etc.)

### Versionamento

- **MAJOR** (X.0.0): Mudanças incompatíveis com versões anteriores
- **MINOR** (0.X.0): Novas funcionalidades compatíveis
- **PATCH** (0.0.X): Correções de bugs

---

## Agradecimentos

Projeto criado com ❤️ usando:

- [LangChain](https://langchain.com)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [OpenAI](https://openai.com)
- [Google Gemini](https://deepmind.google/technologies/gemini/)
- [Pydantic](https://pydantic.dev)
- [httpx](https://www.python-httpx.org)
