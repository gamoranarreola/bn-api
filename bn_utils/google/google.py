import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_calendar_service():

    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)


def handle_calendar_params(calendar):

    return {"id": calendar["id"], "beautier_name": calendar["summary"]}


def handle_free_busy_data(free_busy, calendar_id):

    return {
        "time_min": free_busy["timeMin"],
        "time_max": free_busy["timeMax"],
        "busy": free_busy["calendars"][calendar_id]["busy"],
    }


def handle_events_data(events):

    formatted_events = []

    for item in events["items"]:

        formatted_events.append(
            {
                "id": item["id"],
                "service_name": item["summary"],
                "start": item["start"]["dateTime"],
                "end": item["end"]["dateTime"],
            }
        )

    return formatted_events
