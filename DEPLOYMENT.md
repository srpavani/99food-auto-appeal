# 🚀 Guia de Deployment e Automação

## Executar Automaticamente

### Opção 1: Docker (Recomendado)

#### Executar uma única vez

```bash
docker-compose up
```

#### Executar periodicamente (a cada hora)

Edite `docker-compose.yml`:

```yaml
command: bash -c "while true; do python main.py; sleep 3600; done"
```

Depois:

```bash
docker-compose up -d
```

#### Executar manualmente quando precisar

```bash
# Deixa container rodando mas inativo
docker-compose up -d

# Quando quiser processar contestações:
docker-compose exec contestacao-bot python main.py
```

### Opção 2: Cron (Linux/Mac)

Edite o crontab:

```bash
crontab -e
```

Adicione:

```cron
# Executa todo dia às 9h
0 9 * * * cd /caminho/para/99LANGCORE && /caminho/para/venv/bin/python main.py >> logs/contestacao.log 2>&1

# Executa a cada 3 horas
0 */3 * * * cd /caminho/para/99LANGCORE && /caminho/para/venv/bin/python main.py >> logs/contestacao.log 2>&1

# Executa de segunda a sexta às 8h, 12h e 18h
0 8,12,18 * * 1-5 cd /caminho/para/99LANGCORE && /caminho/para/venv/bin/python main.py >> logs/contestacao.log 2>&1
```

Criar diretório de logs:

```bash
mkdir -p logs
```

### Opção 3: Task Scheduler (Windows)

#### Via PowerShell

Criar tarefa que executa diariamente às 9h:

```powershell
$action = New-ScheduledTaskAction -Execute "python" -Argument "H:\99LANGCORE\main.py" -WorkingDirectory "H:\99LANGCORE"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "99Food-Contestacao" -Action $action -Trigger $trigger -Principal $principal -Settings $settings
```

#### Via Interface Gráfica

1. Abra "Task Scheduler"
2. "Create Basic Task"
3. Nome: "99Food Contestacao"
4. Trigger: Daily (ou escolha)
5. Action: "Start a program"
   - Program: `python`
   - Arguments: `main.py`
   - Start in: `H:\99LANGCORE`
6. Finish

### Opção 4: systemd (Linux - Serviço)

Crie `/etc/systemd/system/contestacao.service`:

```ini
[Unit]
Description=99Food Contestacao Automatica
After=network.target

[Service]
Type=simple
User=seu_usuario
WorkingDirectory=/home/seu_usuario/99LANGCORE
Environment="PATH=/home/seu_usuario/99LANGCORE/venv/bin"
ExecStart=/home/seu_usuario/99LANGCORE/venv/bin/python main.py
Restart=on-failure
RestartSec=3600

[Install]
WantedBy=multi-user.target
```

Ative:

```bash
sudo systemctl daemon-reload
sudo systemctl enable contestacao.service
sudo systemctl start contestacao.service

# Ver logs
sudo journalctl -u contestacao.service -f
```

### Opção 5: PM2 (Node.js Process Manager)

Instale PM2:

```bash
npm install -g pm2
```

Crie `ecosystem.config.js`:

```javascript
module.exports = {
  apps: [{
    name: '99food-contestacao',
    script: 'python',
    args: 'main.py',
    cwd: '/caminho/para/99LANGCORE',
    interpreter: 'none',
    cron_restart: '0 9 * * *',  // Todo dia às 9h
    autorestart: false,
    max_memory_restart: '500M',
    error_file: 'logs/error.log',
    out_file: 'logs/output.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss'
  }]
}
```

Execute:

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Monitoramento

### Adicionar Notificações

#### Telegram

Instale:

```bash
pip install python-telegram-bot
```

Adicione em `main.py`:

```python
import telegram
import asyncio

async def enviar_notificacao(mensagem):
    bot = telegram.Bot(token="SEU_BOT_TOKEN")
    await bot.send_message(chat_id="SEU_CHAT_ID", text=mensagem)

# No final da função main():
if all_passed:
    asyncio.run(enviar_notificacao(
        f"✅ Contestações enviadas: {result['appeals_sent']}"
    ))
else:
    asyncio.run(enviar_notificacao(
        f"⚠️ Erros encontrados: {len(result['errors'])}"
    ))
```

#### Email

Instale:

```bash
pip install sendgrid
```

Adicione em `main.py`:

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def enviar_email(assunto, corpo):
    message = Mail(
        from_email='seu@email.com',
        to_emails='destino@email.com',
        subject=assunto,
        html_content=corpo
    )
    
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    sg.send(message)
```

#### Slack

Instale:

```bash
pip install slack-sdk
```

Adicione:

```python
from slack_sdk import WebClient

def enviar_slack(mensagem):
    client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
    client.chat_postMessage(
        channel='#contestacoes',
        text=mensagem
    )
```

### Health Check

Crie `health_check.py`:

```python
import requests
import sys

try:
    response = requests.get("http://localhost:3002/health", timeout=5)
    if response.status_code == 200:
        print("✅ API 99Food está online")
        sys.exit(0)
    else:
        print(f"⚠️ API retornou status {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"❌ API offline: {e}")
    sys.exit(1)
```

Use antes de executar:

```bash
python health_check.py && python main.py
```

## Logs

### Configurar Logs Persistentes

Edite `main.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

# Adicione no início do main()
log_handler = RotatingFileHandler(
    'logs/contestacao.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
log_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
)
logging.getLogger().addHandler(log_handler)
```

### Visualizar Logs

```bash
# Últimas 50 linhas
tail -n 50 logs/contestacao.log

# Acompanhar em tempo real
tail -f logs/contestacao.log

# Buscar erros
grep ERROR logs/contestacao.log

# Contar contestações enviadas hoje
grep "Contestação enviada com sucesso" logs/contestacao.log | grep "$(date +%Y-%m-%d)" | wc -l
```

## Backup e Recuperação

### Backup das Configurações

```bash
# Criar backup
cp .env .env.backup.$(date +%Y%m%d)

# Restaurar
cp .env.backup.20260128 .env
```

### Backup do Estado

Se quiser salvar o histórico:

```python
# Adicione em agent_graph.py após submit_appeal
import json
from datetime import datetime

def save_state(state):
    filename = f"backups/state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
```

## Segurança em Produção

### 1. Use Secrets Manager

Ao invés de `.env`, use:

- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager
- HashiCorp Vault

### 2. Limite Permissões

```bash
chmod 600 .env  # Apenas owner pode ler/escrever
chmod 700 *.py  # Apenas owner pode executar
```

### 3. Rate Limiting

Adicione delay entre pedidos:

```python
import time

def submit_appeal(self, state):
    # ... código existente ...
    time.sleep(2)  # 2 segundos entre contestações
```

### 4. Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def submit_appeal_with_retry(self, order_id, apply_id, comments):
    return self.api_client.submit_appeal(order_id, apply_id, comments)
```

## Performance

### Processamento Paralelo

Para processar múltiplos pedidos simultaneamente:

```python
import asyncio
import httpx

class AsyncAPIClient:
    def __init__(self, base_url):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def submit_appeal_async(self, order_id, apply_id, comments):
        # ... implementação async ...
        pass

# No grafo, processar em paralelo:
async def process_batch(orders):
    tasks = [process_order(order) for order in orders]
    return await asyncio.gather(*tasks)
```

## Troubleshooting

### Container não inicia

```bash
docker-compose logs contestacao-bot
```

### Cron não executa

Verifique logs:

```bash
grep CRON /var/log/syslog
```

### Task Scheduler falha

Event Viewer → Windows Logs → Application

### Sistema usa muita memória

Reduza `PAGE_SIZE` no `.env`:

```env
PAGE_SIZE=5
```

## Escalabilidade

Para múltiplas lojas:

```yaml
# docker-compose.yml
services:
  loja1:
    build: .
    env_file: .env.loja1
  
  loja2:
    build: .
    env_file: .env.loja2
```

## Custo

Estimativa mensal (100 pedidos/dia):

- GPT-4o: ~$30/mês
- Gemini: Grátis (até 50 req/dia) ou ~$20/mês
- Servidor: $5-10/mês (VPS básico)

**Total**: $25-40/mês
