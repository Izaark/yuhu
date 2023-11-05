from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from tasks.providers import get_title_and_email_from_inactive_tasks

@shared_task
def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )


@shared_task
def check_due_tasks():
    tasks = get_title_and_email_from_inactive_tasks()
    for task in tasks:
        send_mail(
            'Tarea Vencida',
            f'Tu tarea "{task["title"]}" ha vencido.',
            settings.EMAIL_HOST_USER,
            [task["email"]],
            fail_silently=False,
        )
