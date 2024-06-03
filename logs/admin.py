from django.contrib import admin

from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateTimeRangeFilter
from .models import ActionLog
import logs.custom_axes_admin

class ActionLogAdmin(admin.ModelAdmin):

    list_display = (
        "display_user",
        "display_action",
        "display_model",
        "display_object_id",
        "formatted_action_time",
        "display_ip_address",
    )

    fields = [
        "user",
        "action",
        "model",
        "object_id",
        "action_time",
        "ip_address",
        "old_values",
        "new_values",
    ]

    list_filter = [
        "action",
        ("action_time", DateTimeRangeFilter),
        "action_time",
        "model",
    ]

    search_fields = ["user__username", "action", "model", "object_id", "action_time", "ip_address"]

    readonly_fields = [
        "user",
        "action",
        "model",
        "object_id",
        "action_time",
        "ip_address",
    ]

    # date_hierarchy = 'action_time'

    def display_user(self, obj):
        return obj.user.username
    display_user.short_description = 'Usuário'

    def display_action(self, obj):
        return obj.get_action_display()
    display_action.short_description = 'Ação'

    def formatted_action_time(self, obj):
        return obj.action_time.strftime('%d/%m/%Y %H:%M')
    formatted_action_time.short_description = 'Horário'

    def display_model(self, obj):
        return obj.model
    display_model.short_description = 'Tabela'

    def display_object_id(self, obj):
        return obj.object_id
    display_object_id.short_description = 'ID do Objeto'

    def display_ip_address(self, obj):
        return obj.ip_address
    display_ip_address.short_description = 'Endereço IP'


admin.site.register(ActionLog, ActionLogAdmin)
