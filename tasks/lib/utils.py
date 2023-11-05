from tasks.tasks import send_notification_email


def create_notification_email(title: str, email: str):
    subject = "Se ah creado una tarea"
    message = f"Estimado usuario, su tarea {title} ha sido creada"
    recipient_list = [email]
    send_notification_email.delay(subject, message, recipient_list)
