from django.dispatch import receiver
from axes.signals import user_locked_out
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

@receiver(user_locked_out)
def handle_user_locked_out(sender, request, username, **kwargs):
    try:
        user = User.objects.get(username=username)
        user_email = user.email
        subject = 'Sua conta foi bloqueada'
        message = 'Sua conta foi bloqueada devido a muitas tentativas de login malsucedidas. Entre em contato com o administrador.'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        send_mail(subject, message, email_from, recipient_list)
    except User.DoesNotExist:
        pass  # Usuário não encontrado, não faça nada
