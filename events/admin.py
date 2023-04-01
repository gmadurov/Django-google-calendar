from django.contrib import admin
# from google_events.admin import site as admin 

# Changed 
from events.actions import update_google
from events.models import Event

# Register your models here.

# Changed 
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("description", "start_date", "end_date", "google_link")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "summary",
                    "google_link",
                    "description",
                    "start_date",
                    "start_time",
                    "end_date",
                    "end_time",
                    # "recuring",
                    "location",
                    "info",
                )
            },
        ),
    )
    readonly_fields = ("google_link",)
    actions = [
        update_google,
    ]
