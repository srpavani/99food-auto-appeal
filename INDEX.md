# 📚 Índice de Arquivos do Projeto

## 🚀 Começar Aqui

| Arquivo | Descrição | Quando usar |
|---------|-----------|-------------|
| **QUICKSTART.md** | Início rápido em 30 segundos | Quer começar AGORA |
| **README.pt-BR.md** | README completo em português | Primeira leitura |
| **GUIA_INSTALACAO.md** | Instalação passo a passo | Problemas na instalação |

## 🎯 Executar o Sistema

| Arquivo | Descrição | Comando |
|---------|-----------|---------|
| **main.py** | ⭐ Script principal | `python main.py` |
| **test_setup.py** | Testar configuração | `python test_setup.py` |
| **test_llm_only.py** | Testar apenas IA | `python test_llm_only.py` |
| **example_usage.py** | Exemplos de uso | `python example_usage.py` |

## ⚙️ Configuração

| Arquivo | Descrição | Editar? |
|---------|-----------|---------|
| **.env** | 🔐 Configurações e API keys | ✅ SIM - Configure suas chaves |
| **env.example.txt** | Exemplo de .env | ❌ Apenas referência |
| **config.py** | Carrega configurações | ❌ Não precisa editar |

## 🧠 Código Principal

| Arquivo | Descrição | Editar? |
|---------|-----------|---------|
| **agent_graph.py** | Orquestração LangGraph | Para customizar fluxo |
| **llm_client.py** | OpenAI + Gemini | Para mudar prompt da IA |
| **api_client.py** | Cliente HTTP 99Food | Para adicionar endpoints |
| **models.py** | Schemas Pydantic | Se API mudar |

## 📖 Documentação

| Arquivo | Conteúdo | Quando ler |
|---------|----------|------------|
| **README.md** | Documentação em inglês | Se preferir inglês |
| **README.pt-BR.md** | Documentação em português | Leia primeiro! |
| **ARQUITETURA.md** | Como funciona internamente | Quer entender o código |
| **FAQ.md** | Perguntas frequentes | Deu problema? |
| **DEPLOYMENT.md** | Deploy e automação | Colocar em produção |
| **QUICKSTART.md** | Início super rápido | Sem tempo para ler muito |
| **CHANGELOG.md** | Histórico de versões | Ver o que mudou |

## 🛠️ Instalação

| Arquivo | Descrição | Comando |
|---------|-----------|---------|
| **install.ps1** | Instalador Windows | `.\install.ps1` |
| **install.sh** | Instalador Linux/Mac | `bash install.sh` |
| **requirements.txt** | Dependências Python | `pip install -r requirements.txt` |

## 🐳 Docker

| Arquivo | Descrição | Comando |
|---------|-----------|---------|
| **Dockerfile** | Imagem Docker | `docker build -t contestacao .` |
| **docker-compose.yml** | Orquestração | `docker-compose up` |
| **.dockerignore** | Arquivos ignorados | - |

## 📋 Utilitários

| Arquivo | Descrição |
|---------|-----------|
| **.gitignore** | Arquivos ignorados pelo Git |
| **LICENSE** | Licença MIT |

---

## 🎓 Fluxo de Leitura Recomendado

### Para Iniciantes

1. **QUICKSTART.md** - Entender o básico
2. **README.pt-BR.md** - Visão completa
3. **GUIA_INSTALACAO.md** - Instalar passo a passo
4. **FAQ.md** - Resolver dúvidas comuns

### Para Desenvolvedores

1. **README.pt-BR.md** - Contexto geral
2. **ARQUITETURA.md** - Estrutura técnica
3. Ler o código:
   - `config.py` → `models.py` → `api_client.py` → `llm_client.py` → `agent_graph.py` → `main.py`
4. **DEPLOYMENT.md** - Colocar em produção

### Para DevOps

1. **DEPLOYMENT.md** - Tudo sobre deploy
2. **Dockerfile** e **docker-compose.yml**
3. **FAQ.md** seção de troubleshooting

---

## 📊 Estrutura Visual

```
99LANGCORE/
│
├── 🚀 EXECUTAR
│   ├── main.py              (PRINCIPAL)
│   ├── test_setup.py
│   ├── test_llm_only.py
│   └── example_usage.py
│
├── ⚙️ CONFIGURAR
│   ├── .env                 (EDITE ESTE)
│   ├── config.py
│   └── env.example.txt
│
├── 🧠 CÓDIGO
│   ├── agent_graph.py       (Grafo LangGraph)
│   ├── llm_client.py        (IA)
│   ├── api_client.py        (HTTP)
│   └── models.py            (Schemas)
│
├── 📖 DOCUMENTAÇÃO
│   ├── README.pt-BR.md      (LEIA PRIMEIRO)
│   ├── QUICKSTART.md        (INÍCIO RÁPIDO)
│   ├── GUIA_INSTALACAO.md
│   ├── ARQUITETURA.md
│   ├── FAQ.md
│   ├── DEPLOYMENT.md
│   └── CHANGELOG.md
│
├── 🛠️ INSTALAÇÃO
│   ├── install.ps1          (Windows)
│   ├── install.sh           (Linux/Mac)
│   └── requirements.txt
│
└── 🐳 DOCKER
    ├── Dockerfile
    ├── docker-compose.yml
    └── .dockerignore
```

---

## 🔍 Busca Rápida

### "Como eu..."

- **...instalo?** → `GUIA_INSTALACAO.md`
- **...configuro?** → Edite `.env` (veja `QUICKSTART.md`)
- **...executo?** → `python main.py`
- **...testo?** → `python test_setup.py`
- **...customizo o prompt da IA?** → `llm_client.py` linha ~40
- **...mudo o fluxo?** → `agent_graph.py`
- **...coloco em produção?** → `DEPLOYMENT.md`
- **...resolvo erros?** → `FAQ.md`
- **...entendo como funciona?** → `ARQUITETURA.md`
- **...adiciono novo provedor de IA?** → `ARQUITETURA.md` seção "Escalabilidade"
- **...uso Docker?** → `docker-compose up` (veja `DEPLOYMENT.md`)

### "Deu erro..."

- **...de API key** → Confira `.env`
- **...de conexão** → Veja `FAQ.md` → "Connection refused"
- **...na instalação** → `GUIA_INSTALACAO.md` → Troubleshooting
- **...desconhecido** → Execute `python test_setup.py` e leia os logs

---

## 📞 Precisa de Ajuda?

1. **Primeiro**: Leia `FAQ.md` - 90% das dúvidas estão lá
2. **Segundo**: Execute `python test_setup.py` para diagnosticar
3. **Terceiro**: Leia a documentação específica do erro
4. **Quarto**: Verifique os logs no terminal

---

**Última atualização**: 2026-01-28
**Versão**: 1.0.0
