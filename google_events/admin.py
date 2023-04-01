import json
import os
from datetime import date, datetime, time, timedelta

from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from django.views.generic import ListView
# import time
from events.signals import get_service
from events.models import Event

class MyAdminSite(admin.AdminSite):

    def get_urls(self):
        self._registry = admin.site._registry
        custom_urls = [
            path(
                "google/",
                GoogleAgenda.as_view(admin=self),
                name="preferences",
            ),
        ]
        admin_urls = super().get_urls()
        return custom_urls + admin_urls  # custom urls must be at the beginning

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_list += [
            {
                "name": "Google",
                "app_label": "Google Events",
                # "app_url": "/admin/test_view",
                "models": [
                    {
                        "name": "Google Events",
                        "object_name": "Google Events",
                        "admin_url": "/google",
                        "view_only": True,
                    }
                ],
            }
        ]
        return app_list


site = MyAdminSite()


def get_events(agenda_id):
    service = get_service()
    return (
        service.events()
        .list(
            calendarId=agenda_id,
            maxResults=2499,
            orderBy="startTime",
            singleEvents=True,
            timeMin=(datetime.today() - timedelta(days=90)).isoformat() + "Z",
        )
        .execute()
    )


class GoogleAgenda(ListView):
    admin = {}

    def get(self, request):
        ctx = self.admin.each_context(request)
        events = get_events(os.environ.get("calendarId", 'primary')).get("items", [])
        event_google_ids = Event.objects.values_list("google_link", flat=True)
        ctx["events"] = events
        ctx["event_google_ids"] = event_google_ids
        return render(request, "events/google_events.html", ctx)
