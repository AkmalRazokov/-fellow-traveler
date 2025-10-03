from fastapi_mail import FastMail, MessageSchema
from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="rmaks8048@gmail.com",
    MAIL_PASSWORD="qflujqieyjakzqqf",
    MAIL_FROM="rmaks8048@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Ak",
    MAIL_SSL_TLS=False, 
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)





async def send_email(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to], 
        body=body,
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
