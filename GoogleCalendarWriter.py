import datetime
import pickle
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarWriter:
    def __init__(self):
        self._service = None
    
    def authenticate(self):
        """Authenticating a user and returning a Google Calendar service"""
        creds = None
        if os.path.exists("cal_token.pickle"):
            with open("cal_token.pickle", "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("cal_credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("cal_token.pickle", "wb") as token:
                pickle.dump(creds, token)
        self._service = build("calendar", "v3", credentials=creds)

    def get_upcoming_events(self, amountOfEvents):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print("Getting upcoming {} events".format(amountOfEvents))
        events_result = self._service.events().list(calendarId="primary", timeMin=now, maxResults=amountOfEvents, singleEvents=True, orderBy="startTime").execute()
        events = events_result.get("items", [])
        if not events:
            print("No upcoming events found")
        for event in events:
            start = event["start"].get("datetime", event["start"].get("date"))
            print("Date {} : Task {}".format(start, event["summary"]))

    def add_events_to_calendar(self, events):
        print("Adding {} daily events to your Calendar".format(len(events)))
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        end_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=10)).isoformat()[:19] + "Z"
        for key, value in events.items():
            event = {
                'summary': str(value),
                'location': 'Lincoln, UK',
                'description': str(value),
                'start': {
                    'dateTime': str(now[:11]) + str(key) + ":00Z",
                    'timeZone': 'Europe/London',
                },
                "end": {
                    'dateTime': str(end_time),
                    'timeZone': 'Europe/London',
                }
            }
            print(event)
            event = self._service.events().insert(calendarId="primary", body=event).execute()
            print("Event created : %s" % (event.get("htmlLink")))

# 2020-08-24T07:30:00-00:00
# 2015-05-28T09:00:00-07:00