import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

# Retorna o JSON com os dados novos
def serialize_instance(instance):
    data = {}
    for field in instance._meta.fields:
        value = getattr(instance, field.name)
        if isinstance(value, models.Model):
            data[field.name] = str(value)  # Convert related model instances to string
        else:
            data[field.name] = value
    return json.dumps(data, cls=DjangoJSONEncoder, ensure_ascii=False)

# Retorna o JSON com os dados antigos
def serialize_changed_fields(instance):
    data = {}
    dirty_fields = instance.get_dirty_fields()

    # Cria o resultset com todos os campos
    for field in instance._meta.fields:
        value = getattr(instance, field.name)
        if isinstance(value, models.Model):
            data[field.name] = str(value)  # Convert related model instances to string
        else:
            data[field.name] = value

    # Percorre todos os campos com valor alterado e sobrescreve no resultset, para ficar com os dados antigos
    for field, old_value in dirty_fields.items():
        current_value = getattr(instance, field)
        if isinstance(current_value, models.Model):
            data[field] = str(old_value)
        else:
            data[field] = old_value
    return json.dumps(data, cls=DjangoJSONEncoder, ensure_ascii=False)
