# Generated by Django 5.0.6 on 2024-06-02 17:48

import dirtyfields.dirtyfields
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=10)),
                ('model', models.CharField(max_length=50)),
                ('object_id', models.CharField(max_length=50)),
                ('action_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip_address', models.GenericIPAddressField()),
                ('old_values', models.TextField(blank=True, null=True)),
                ('new_values', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
