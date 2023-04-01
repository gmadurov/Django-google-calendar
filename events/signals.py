"""
This file contains the signals that are used to update the google agenda when an event is created or deleted in the website
This file has been added on top of the events app
"""


import json
import os
from datetime import datetime, time

# import time
from django.db.models.signals import post_delete, post_save
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

from .models import Event


def get_service(refresh=False):
    try:
        cred_json = json.loads(os.environ.get("client_secret", ""))
    except:
        print("client_secret not retrieved")
        pass
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        cred_json
    )
    service = build("calendar", "v3", credentials=credentials)
    return service


def google_handle_event(sender, created, instance: Event, **kwargs):
    """this function creates the events in the google agenda and updates them if changed in the website"""
    if os.environ.get("UPDATE_GOOGLE", "") in [False, 0, "False"]:
        return
    service = get_service()
    event = instance
    if not event.end_date:
        event.end_date = event.start_date
    if not event.start_time:
        event.start_time = time(20, 0)
    if not event.end_time:
        event.end_time = time(23, 59, 0)
    if event.end_date < event.start_date:
        event.end_date, event.start_date = event.start_date, event.end_date
    queryset = Event.objects.filter(
        id=event.id
    )  # https://stackoverflow.com/questions/1555060/how-to-save-a-model-without-sending-a-signal
    # this is used so that we can update the google event within this signal without reshooting this signal(signals shot every time an object is saved)

    event_body = {
        "summary": event.summary,
        "location": event.location or "",
        "description": f"{event.description} ({event.summary}) \n{'Extra info: '+event.info if event.info else ''}",
        "start": {
            "dateTime": datetime.combine(
                event.start_date, event.start_time
            ).isoformat(),
            "timeZone": "Europe/Amsterdam",
        },
        "end": {
            "dateTime": datetime.combine(event.end_date, event.end_time).isoformat(),
            "timeZone": "Europe/Amsterdam",
        },
        "recurrence": [],
        "reminders": {},
    }

    if created or not instance.google_link:
        try:
            google_event = (
                service.events()
                .insert(
                    calendarId=os.environ.get("calendarId", "primary"),
                    body=event_body,
                )
                .execute()
            )
            queryset.update(
                google_link=google_event["id"],
                start_date=event.start_date,
                start_time=event.start_time,
                end_date=event.end_date,
                end_time=event.end_time,
            )

        except HttpError as error:
            print("An error occurred:1 %s" % error)
    else:
        try:
            google_event = (
                service.events()
                .update(
                    calendarId=os.environ.get("calendarId", "primary"),
                    body=event_body,
                    eventId=event.google_link,
                )
                .execute()
            )
            print(google_event)
            queryset.update(
                google_link=google_event["id"],
                start_date=event.start_date,
                start_time=event.start_time,
                end_date=event.end_date,
                end_time=event.end_time,
            )

        except HttpError as error:
            print("An error occurred:2 %s" % error)
            pass


def google_delete_event(sender, instance, **kwargs):
    """this function deletes an event from google agenda whendeleted in the website"""
    if os.environ.get("UPDATE_GOOGLE") in [False, 0, "False"]:
        return
    try:
        service = get_service()
        service.events().delete(
            calendarId=os.environ.get("calendarId", "primary"),
            eventId=instance.google_link,
        ).execute()
    except:
        pass


post_save.connect(google_handle_event, sender=Event)
post_delete.connect(google_delete_event, sender=Event)
