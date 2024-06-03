from axes.admin import AccessAttemptAdmin, AccessLogAdmin
from django.contrib import admin

from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from axes.conf import settings
from axes.models import AccessAttempt, AccessLog
from rangefilter.filters import DateTimeRangeFilter

class CustomAccessAttemptAdmin(AccessAttemptAdmin):
    list_display = (
        "ip_address",
        "username",
        "formatted_attempt_time",
        "failures_since_start",
        "user_agent",
    )

    list_filter = ["attempt_time", ("attempt_time", DateTimeRangeFilter), "path_info"]

    search_fields = ["ip_address", "username", "user_agent", "path_info"]

    date_hierarchy = "attempt_time"

    fieldsets = (
        (None, {"fields": ("username", "path_info", "failures_since_start")}),
        (_("Form Data"), {"fields": ("get_data", "post_data")}),
        (_("Meta Data"), {"fields": ("user_agent", "ip_address", "http_accept")}),
    )

    readonly_fields = [
        "user_agent",
        "ip_address",
        "username",
        "http_accept",
        "path_info",
        "attempt_time",
        "get_data",
        "post_data",
        "failures_since_start",
    ]

    def formatted_attempt_time(self, obj):
        return obj.attempt_time.strftime('%d/%m/%Y %H:%M')
    formatted_attempt_time.short_description = 'Attempt Time'

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


class CustomAccessLogAdmin(AccessLogAdmin):
    list_display = (
        "ip_address",
        "username",
        "formatted_attempt_time",
        "formatted_logout_time",
        "display_uptime",
        "user_agent",
    )

    list_filter = ["attempt_time", ("attempt_time", DateTimeRangeFilter), "logout_time", "path_info"]

    search_fields = ["ip_address", "user_agent", "username", "path_info"]

    date_hierarchy = "attempt_time"

    fieldsets = (
        (None, {"fields": ("username", "path_info")}),
        (_("Meta Data"), {"fields": ("user_agent", "ip_address", "http_accept")}),
    )

    readonly_fields = [
        "user_agent",
        "ip_address",
        "username",
        "http_accept",
        "path_info",
        "attempt_time",
        "logout_time",
    ]

    def formatted_attempt_time(self, obj):
        return obj.attempt_time.strftime('%d/%m/%Y %H:%M')
    formatted_attempt_time.short_description = 'Attempt Time'

    def formatted_logout_time(self, obj):
        if obj.logout_time:
            return obj.logout_time.strftime('%d/%m/%Y %H:%M')
        return obj.logout_time
    formatted_logout_time.short_description = 'Logout Time'

    def display_uptime(self, obj):
        if obj.uptime:
            total_seconds = int(obj.uptime.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return obj.uptime
    display_uptime.short_description = 'Duration'

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

if settings.AXES_ENABLE_ADMIN:
    admin.site.unregister(AccessAttempt)
    admin.site.register(AccessAttempt, CustomAccessAttemptAdmin)

    admin.site.unregister(AccessLog)
    admin.site.register(AccessLog, CustomAccessLogAdmin)
