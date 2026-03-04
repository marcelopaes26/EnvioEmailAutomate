# EnvioEmailAutomate

Automação em Python para **abrir composições de e-mail automaticamente no 1º dia útil do mês**, já com **destinatários, CC, assunto e corpo preenchidos**, solicitando relatórios referentes ao mês anterior.

O script utiliza `mailto:` para abrir o **cliente de e-mail padrão do sistema** (Outlook, Gmail Desktop, etc.) e registra logs de execução.

---

## O que este projeto faz

- Verifica se **hoje é o primeiro dia útil do mês** (considerando finais de semana e feriados nacionais do Brasil).
- Caso não seja o primeiro dia útil, o script encerra silenciosamente.
- Calcula automaticamente o **mês anterior** no formato `MM/YYYY`.
- Abre janelas de composição de e-mail já preenchidas com **destinatários, CC, assunto e corpo do e-mail**.
- Registra logs de execução em arquivo.
- Realiza **arquivamento anual do log** no primeiro dia útil de janeiro.

---

## Pré-requisitos

- Python 3.10 ou superior

Bibliotecas utilizadas:

- python-dotenv
- holidays

Instalação:

```bash
pip install python-dotenv holidays
```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Pasta onde os logs serão armazenados
LOGS=C:\caminho\para\logs

# Destinatários
EMAIL_TO_DROID=exemplo@dominio.com
EMAIL_TO_DP=exemplo@dominio.com

# CC (opcional)
EMAIL_CC=exemplo@dominio.com
```

---

## Como executar

Execute o script:

```bash
python script.py
```

### Comportamento esperado

- Se **não for o primeiro dia útil do mês**, o script apenas encerra.
- Se **for o primeiro dia útil**, o script abrirá automaticamente as janelas de composição de e-mail no cliente padrão do sistema.

Basta revisar a mensagem e clicar em **Enviar**.

---

## Logs

Os logs são armazenados no diretório definido na variável `LOGS`.

Arquivo padrão:

```
run.log
```

No primeiro dia útil de janeiro, caso exista `run.log`, ele será renomeado automaticamente para:

```
run-ANO.log
```

Isso mantém um histórico anual das execuções.

---

## Sugestão de automação

O script pode ser configurado no **Windows Task Scheduler (Agendador de Tarefas)** para rodar automaticamente todos os dias.

Mesmo sendo executado diariamente, ele **só realizará a ação no primeiro dia útil do mês**, evitando envios duplicados.

---

## Estrutura do projeto

```
.
├── script.py
└── .gitignore
```

---

## Observações

- O script **não envia o e-mail automaticamente** via SMTP.
- Ele apenas abre a composição no cliente padrão usando `mailto:`.
- Isso permite revisar a mensagem antes do envio.
