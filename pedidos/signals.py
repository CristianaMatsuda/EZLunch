from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Pedido
from django.conf import settings

@receiver(post_save, sender=Pedido)
def notify_user_order_status_change(sender, instance, **kwargs):
    if instance.pk and 'status' in instance.get_dirty_fields():
        user_email = instance.cliente.email
        subject = f'Status do Pedido #{instance.id} Atualizado'
        message = f'O status do seu pedido foi atualizado para: {instance.get_status_display()}'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        send_mail(subject, message, email_from, recipient_list)
