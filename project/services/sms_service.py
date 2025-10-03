from twilio.rest import Client
from decouple import config



def send_sms(phone: str, code: str):
    print(f"[ТЕСТОВЫЙ РЕЖИМ] Код для {phone}: {code}")
