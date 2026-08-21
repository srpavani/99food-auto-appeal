# 🔄 Modo Contínuo - Sistema de Contestação Automática

## O que mudou?

O sistema agora funciona em **modo contínuo**, buscando pedidos automaticamente a cada 15 minutos!

### Novos Recursos

✅ **Execução Contínua**: Roda em loop infinito, buscando pedidos a cada 15 minutos  
✅ **Data Dinâmica**: Busca automaticamente os últimos 7 dias (não precisa configurar datas no .env)  
✅ **Controle de Duplicação**: Nunca contesta o mesmo pedido duas vezes  
✅ **Database JSON**: Armazena histórico de pedidos processados  
✅ **Logs Detalhados**: Salva tudo em arquivos TXT para auditoria  

## Como Usar

### Modo Contínuo (Recomendado)

Deixa o sistema rodando e ele busca pedidos automaticamente:

```bash
python main.py
```

O sistema irá:
1. Buscar pedidos dos últimos 7 dias
2. Contestar os que ainda não foram processados
3. Aguardar 15 minutos
4. Repetir infinitamente

**Para parar:** Pressione `Ctrl+C`

### Modo Uma Vez (Manual)

Se quiser rodar apenas uma vez:

```bash
python main_once.py
```

Útil para:
- Testar manualmente
- Executar via cron/task scheduler
- Integrar com outros sistemas

## Estrutura de Arquivos

### Database (JSON)

```
data/
└── processed_orders.json
```

Armazena:
- Todos os pedidos já contestados
- Data de processamento
- Se foi sucesso ou falha
- Estatísticas gerais

**Exemplo:**

```json
{
  "processed_orders": {
    "5764655711753670171_5764655887968964208": {
      "order_id": "5764655711753670171",
      "apply_id": "5764655887968964208",
      "reason": "Itens incorretos",
      "defense": "Consideramos improvável...",
      "success": true,
      "processed_at": "2026-01-28T21:30:00",
      "timestamp": 1738102200.0
    }
  },
  "stats": {
    "total_processed": 1
  }
}
```

### Logs Detalhados (TXT)

```
logs/
├── contestacoes_2026-01-28.txt
└── ciclos_2026-01-28.txt
```

#### Arquivo de Contestações

Cada contestação é salva com detalhes completos:

```
================================================================================
CONTESTAÇÃO REGISTRADA
================================================================================
Data/Hora: 28/01/2026 21:30:00
Pedido ID: 5764655711753670171
Apply ID: 5764655887968964208

--------------------------------------------------------------------------------
DADOS DO PEDIDO
--------------------------------------------------------------------------------
Motivo da Reclamação: Itens incorretos
Itens do Pedido: Cachorro Quente Duplo x3
Imagem de Prova: SIM - https://img0.didiglobal.com/static/...

--------------------------------------------------------------------------------
PROMPT ENVIADO PARA IA
--------------------------------------------------------------------------------
Motivo da reclamação: Itens incorretos
Itens do pedido: Cachorro Quente Duplo x3
Imagem: https://img0.didiglobal.com/static/...

--------------------------------------------------------------------------------
RESPOSTA DA IA
--------------------------------------------------------------------------------
Consideramos improvável. A imagem mostra produtos corretos. Pedidos são
conferidos antes do envio.

--------------------------------------------------------------------------------
RESULTADO
--------------------------------------------------------------------------------
Status: ✅ ENVIADO COM SUCESSO

================================================================================
```

#### Arquivo de Ciclos

Resumo de cada execução:

```
============================================================
CICLO #1 - 28/01/2026 21:30:00
============================================================
📊 Pedidos encontrados: 9
✅ Processados neste ciclo: 3
⏭️  Pulados (já contestados): 6
❌ Erros: 0
============================================================
```

## Funcionamento do Controle de Duplicação

### Como Funciona?

1. **Antes de contestar**: Sistema verifica no database se `{order_id}_{apply_id}` já existe
2. **Se já existe**: Pula o pedido (não contesta novamente)
3. **Se não existe**: Processa normalmente
4. **Após contestar**: Salva no database (mesmo se falhou)

### Por que salvar mesmo se falhou?

Para evitar tentar contestar infinitamente um pedido que sempre falha (ex: pedido inválido na API).

### Resetar Database

Se quiser reprocessar todos os pedidos:

```bash
# Fazer backup primeiro
cp data/processed_orders.json data/processed_orders.backup.json

# Deletar database
rm data/processed_orders.json

# Na próxima execução, um novo database será criado
```

## Logs no Terminal

### Exemplo de Execução

```
======================================================================
🤖 SISTEMA DE CONTESTAÇÃO AUTOMÁTICA - 99FOOD (MODO CONTÍNUO)
======================================================================

🔧 Configurações:
   - Provedor LLM: OPENAI
   - Modelo: gpt-4o
   - API Base: http://localhost:3002
   - Intervalo: A cada 15 minutos
   - Busca: Últimos 7 dias (dinâmico)

📊 Estatísticas do Database:
   - Total processado: 12
   - Sucessos: 11
   - Falhas: 1
   - Último processamento: 2026-01-28T20:15:00

======================================================================
🔄 MODO CONTÍNUO ATIVADO
======================================================================
O sistema irá buscar pedidos a cada 15 minutos.
Pressione Ctrl+C para parar.


======================================================================
🔄 CICLO #1 - 28/01/2026 21:30:00
======================================================================

📅 Período: 2026-01-21 até 2026-01-28
🔍 Buscando pedidos com reembolso...
✅ Encontrados 9 pedidos com reembolso

📄 Buscando detalhes do pedido 5764655711753670171...
⏭️  Pedido 5764655711753670171 já foi contestado anteriormente, pulando...

📄 Buscando detalhes do pedido 5764656253489971683...
📋 Motivo: Produto não chegou
🖼️  Imagem: NÃO

🤖 Gerando defesa com IA...
💬 Defesa gerada: Confirmamos que o pedido foi despachado e entregue...

📤 Enviando contestação...
✅ Contestação enviada com sucesso para pedido 5764656253489971683

----------------------------------------------------------------------
📊 RESUMO DO CICLO #1
----------------------------------------------------------------------
📋 Pedidos encontrados: 9
✅ Contestações enviadas: 1
⏭️  Pedidos pulados (já contestados): 8
❌ Erros: 0

📊 Estatísticas Gerais:
   - Total processado: 13
   - Processado hoje: 5
----------------------------------------------------------------------

⏰ Próxima execução em 15 minutos (21:45:00)
   Pressione Ctrl+C para parar.
```

## Monitoramento

### Ver Estatísticas

```bash
# Ver database completo
cat data/processed_orders.json

# Contar pedidos processados hoje
python -c "from database import OrderDatabase; db = OrderDatabase(); print(db.get_processed_count_today())"

# Ver último log de contestações
tail -n 50 logs/contestacoes_$(date +%Y-%m-%d).txt

# Ver resumo de ciclos de hoje
cat logs/ciclos_$(date +%Y-%m-%d).txt
```

### Logs em Tempo Real

```bash
# Acompanhar contestações
tail -f logs/contestacoes_$(date +%Y-%m-%d).txt

# Acompanhar ciclos
tail -f logs/ciclos_$(date +%Y-%m-%d).txt
```

## Configurações

### Mudar Intervalo de Busca

Edite `main.py`, linha ~85:

```python
# Aguarda 15 minutos (900 segundos)
wait_seconds = 900  # Mude para o valor desejado em segundos
```

**Exemplos:**
- 5 minutos: `300`
- 30 minutos: `1800`
- 1 hora: `3600`

### Mudar Período de Busca

Edite `main.py`, linha ~21:

```python
def get_date_range(days_back: int = 7):  # Mude aqui
```

**Exemplos:**
- Últimos 3 dias: `days_back=3`
- Último dia: `days_back=1`
- Últimas 2 semanas: `days_back=14`

## Executar como Serviço

### Docker (Recomendado)

```bash
# Modo contínuo
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### systemd (Linux)

```bash
# Usar main.py que já tem loop infinito
sudo systemctl start contestacao
sudo systemctl enable contestacao
```

### Task Scheduler (Windows)

Para modo contínuo, deixe o script rodando:

1. Crie um script `start.bat`:

```batch
@echo off
cd H:\99LANGCORE
python main.py
pause
```

2. Execute o `.bat` manualmente ou configure para iniciar com o Windows

### Cron (modo manual, sem loop)

Se preferir usar cron ao invés do loop interno:

```cron
# A cada 15 minutos
*/15 * * * * cd /path/to/99LANGCORE && python main_once.py >> logs/cron.log 2>&1
```

## Vantagens do Modo Contínuo

✅ **Automático**: Não precisa lembrar de rodar  
✅ **Imediato**: Contesta em até 15 minutos após pedido chegar  
✅ **Seguro**: Nunca duplica contestações  
✅ **Auditável**: Logs completos de tudo  
✅ **Resiliente**: Continua rodando mesmo com erros  

## Troubleshooting

### Sistema não está buscando pedidos

Verifique se a API 99Food está online:

```bash
curl http://localhost:3002/orders/refunds
```

### Contestando o mesmo pedido duas vezes

Verifique se o database existe:

```bash
ls -la data/processed_orders.json
```

Se não existir, será criado automaticamente.

### Logs não estão sendo salvos

Verifique permissões:

```bash
mkdir -p logs data
chmod 755 logs data
```

### Quer limpar tudo e recomeçar

```bash
# Backup
cp -r data data.backup
cp -r logs logs.backup

# Limpar
rm -rf data/* logs/*

# Sistema criará novos na próxima execução
```

## Diferenças entre main.py e main_once.py

| Característica | main.py | main_once.py |
|----------------|---------|--------------|
| Execução | Loop infinito | Uma vez |
| Intervalo | A cada 15 min | - |
| Uso | Deixar rodando | Manual/Cron |
| Parar | Ctrl+C | Termina sozinho |
| Ideal para | Servidor/Docker | Testes/Cron |

## Próximos Passos

Após configurar o modo contínuo:

1. **Monitore os logs** nas primeiras horas
2. **Verifique o database** `data/processed_orders.json`
3. **Confira as contestações** em `logs/contestacoes_*.txt`
4. **Ajuste o intervalo** se necessário
5. **Configure alertas** (Telegram, email, etc.)

---

**Dúvidas?** Leia `FAQ.md` ou `GUIA_INSTALACAO.md`
