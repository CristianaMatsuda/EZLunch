# logs/signals.py

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import ActionLog
from .middleware import get_current_user, get_ip_address, _thread_locals
from .utils import serialize_instance, serialize_changed_fields
from pedidos.models import Categoria, Conteudo, Tamanho, Marmita, Pedido, Item

@receiver(post_save, sender=Categoria)
@receiver(post_save, sender=Conteudo)
@receiver(post_save, sender=Tamanho)
@receiver(post_save, sender=Marmita)
@receiver(post_save, sender=Pedido)
@receiver(post_save, sender=Item)
def log_save(sender, instance, created, **kwargs):
    action = 'C' if created else 'U'

    user = get_current_user()
    request = getattr(_thread_locals, 'request', None)
    ip_address = get_ip_address(request)

    new_values = serialize_instance(instance)
    old_values = None

    if action == 'U' and hasattr(instance, 'get_dirty_fields'):
        old_values = serialize_changed_fields(instance)

    ActionLog.objects.create(
        user=user,
        action=action,
        model=sender.__name__,
        object_id=instance.pk,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address
    )

@receiver(pre_delete, sender=Categoria)
@receiver(pre_delete, sender=Conteudo)
@receiver(pre_delete, sender=Tamanho)
@receiver(pre_delete, sender=Marmita)
@receiver(pre_delete, sender=Pedido)
@receiver(pre_delete, sender=Item)
def log_delete(sender, instance, **kwargs):
    user = get_current_user()
    request = getattr(_thread_locals, 'request', None)
    ip_address = get_ip_address(request)
    old_values = serialize_instance(instance)

    ActionLog.objects.create(
        user=user,
        action='D',
        model=sender.__name__,
        object_id=instance.pk,
        old_values=old_values,
        new_values=None,
        ip_address=ip_address
    )
