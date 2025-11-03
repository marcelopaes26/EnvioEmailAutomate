from datetime import datetime, timedelta, date
import webbrowser
import urllib.parse
import time
import os
import logging
from dotenv import load_dotenv
import sys
import holidays

# ENV
load_dotenv()
LOGDIR = os.getenv('LOGS')
EMAIL_TO_DROID = os.getenv('EMAIL_TO_DROID')
EMAIL_TO_DP = os.getenv('EMAIL_TO_DP')
EMAIL_CC = os.getenv('EMAIL_CC')

# CONFIG
PAUSE_SECONDS = 0.6  # pausa entre abrir composições
HOJE_TIME = datetime.now()
HOJE_DATE = HOJE_TIME.date()
FERIADOS = holidays.Brazil(years=[HOJE_DATE.year]) # feriados do ano

# DIA ÚTIL
def is_business_day(d: date, feriados: holidays.HolidayBase) -> bool:
    return d.weekday() < 5 and d not in feriados

# 1º DIA ÚTIL DO MÊS
def first_business_day_of_month(y: int, m: int, feriados: holidays.HolidayBase) -> date:
    d = date(y, m, 1)
    while not is_business_day(d, feriados):
        d += timedelta(days=1)
    return d

# Verifica se é o 1º dia útil, se não for já encerra o sistema silenciosamente
first_bd = first_business_day_of_month(HOJE_DATE.year, HOJE_DATE.month, FERIADOS)
if HOJE_DATE != first_bd:
    sys.exit(0)

# LOGGING
os.makedirs(LOGDIR, exist_ok=True)
logfile = os.path.join(LOGDIR, "run.log")

first_bday_jan = first_business_day_of_month(HOJE_DATE.year, 1, FERIADOS)

# Arquivamento anual de log (1 de Janeiro)
if HOJE_DATE == first_bday_jan and os.path.exists(logfile):
    nome_arquivo = os.path.join(LOGDIR, f"run-{HOJE_DATE.year-1}.log")
    try:
        os.rename(logfile, nome_arquivo)
        print(f"[INFO] Log arquivado: {nome_arquivo}")
    except Exception as e:
        print(f"[WARN] Não foi possível arquivar o log: {e}")


fh = logging.FileHandler(logfile, encoding="utf-8")
ch = logging.StreamHandler()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[fh, ch]
)

log = logging.getLogger("mailto")

# calcula mês anterior no formato MM/YYYY
def mes_anterior():
    primeiro_deste_mes = HOJE_TIME.replace(day=1)
    ultimo_mes = primeiro_deste_mes - timedelta(days=1)
    return ultimo_mes.strftime("%m/%Y")  # ex.: "08/2025"

# Verifica hora atual para saudação
def saudacao_atual():
    return "Bom dia" if HOJE_TIME.hour < 12 else "Boa tarde"

def open_mailto(to, cc, subject, body):
    # codifica os componentes para URL
    params = {
        "subject": subject,
        "body": body
    }
    if cc:
        params["cc"] = cc
    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    # to não deve ser codificado com urlencode como parte do query; codificamos separadamente
    to_enc = urllib.parse.quote(to)
    mailto = f"mailto:{to_enc}?{query}"
    webbrowser.open(mailto, new=1)

if __name__ == "__main__":
    
    try:
        
        mes_anterior_str = mes_anterior()
        saudacao = saudacao_atual()
        
        # Mensagens: campos curtos (ideais para mailto)
        mensagens = [
            {
                "to": f"{EMAIL_TO_DROID}",
                "cc": f"{EMAIL_CC}",
                "subject": f"Relatório LSE - Mês {mes_anterior_str}",
                "body": (
                    f"{saudacao}, tudo bem?\n\n"
                    f"Poderiam nos encaminhar o relatório do LSE do mês anterior ({mes_anterior_str}), por gentileza?\n\n"
                    "Desde já, agradecemos."
                ),
            },
            {
                "to": f"{EMAIL_TO_DP}",
                "cc": f"{EMAIL_CC}",
                "subject": f"Relação de Agentes e Colaboradores - Mês {mes_anterior_str}",
                "body": (
                    f"{saudacao}, tudo bem?\n\n"
                    f"Poderiam nos encaminhar a relação do número de agentes atuantes e a relação dos colaboradores até o último dia do mês anterior ({mes_anterior_str}), por gentileza?\n\n"
                    "Desde já, agradecemos."
                ),
            },
        ]
        
        log.info(f"INÍCIO | mês_anterior={mes_anterior_str} | total_msgs={len(mensagens)}")
        
        for i, m in enumerate(mensagens, start=1):
            try:
                log.info(f"[{i}/{len(mensagens)}] Abrindo compose: to='{m['to']}' cc='{m.get('cc','')}' subject='{m['subject']}'")
                open_mailto(m["to"], m.get("cc", ""), m["subject"], m["body"])
                time.sleep(PAUSE_SECONDS)
                log.info(f"[{i}/{len(mensagens)}] Compose solicitado com sucesso (aguardando clique em Enviar).")
            except Exception as e:
                log.exception(f"[{i}/{len(mensagens)}] Falha ao abrir compose: {e}")
                sys.exit(1)
                
        log.info("FIM | Todas as composições foram solicitadas ao cliente de e-mail padrão.")
        sys.exit(0)
    
    except SystemExit as se:
        raise se
    except Exception as e:
        log.exception(f"ERRO FATAL: {e}")
        sys.exit(1)