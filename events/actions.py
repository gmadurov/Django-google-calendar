'''
This file is for the actions in the admin panel
This file has been added on top of the events app
'''


from .models import Event
from .signals import google_handle_event

# Changed 

def update_google(modeladmin, request, queryset):
    event: Event
    for event in queryset:
        google_handle_event(None, False, event)