from celery import Celery
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import Config

celery = Celery('tasks', broker=Config.CELERY_BROKER_URL)
celery.conf.update(result_backend=Config.CELERY_RESULT_BACKEND)

@celery.task
def enviar_email_task(to_email, subject, content):
    sg = SendGridAPIClient(api_key=Config.SENDGRID_API_KEY)
    email = Mail(
        from_email='seu-email@exemplo.com',
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    sg.send(email)
    return 'Email enviado com sucesso!'