from django.contrib import admin
from .models import Roll


@admin.register(Roll)
class RollAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "set_number",
        "stand_number",
        "profile",
        "current_diameter",
        "current_status",
    )

    search_fields = (
        "number",
        "set_number",
        "profile",
    )

    list_filter = (
        "current_status",
        "stand_number",
    )
