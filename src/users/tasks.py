from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives



@shared_task()
def send_otp_to_email(email, otp):
    subject = 'Восстановление пароля!'
    from_mail = settings.EMAIL_HOST_USER
    to_list = [email, ]
    text = f'Ваш код для смены пароля: {otp}'
    msg = EmailMultiAlternatives(subject, text, from_mail, to_list)
    msg.send()
