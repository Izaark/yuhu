from tasks.tasks import send_notification_email


def create_notification_email(title: str, email: str, action: str):
    subject = f"La tarea {title} se ah {action}"
    message = f"Estimado usuario, su tarea con el titulo {title} se ah {action}"
    recipient_list = [email]
    send_notification_email.delay(subject, message, recipient_list)
