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
        self._timePerTask = 10
    

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
        """
        Retrieves a list of the upcoming events
        based on the value set in the parameter
        """
        print("Getting upcoming {} events".format(amountOfEvents))
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self._service.events().list(calendarId="primary", timeMin=now, maxResults=amountOfEvents, singleEvents=True, orderBy="startTime").execute()
        events = events_result.get("items", [])
        if not events:
            print("No upcoming events found")
        for event in events:
            start = event["start"].get("datetime", event["start"].get("date"))
            print("Date {} : Task {}".format(start, event["summary"]))


    def add_events_to_calendar(self, events):
        """
        Adds daily events to the calender,
        deals with timestamps and dates
        """
        print("Adding {} daily events to your Calendar".format(len(events)))
        now = datetime.datetime.utcnow().isoformat()
        for key, value in events.items():
            now = str(now[:11]) + str(key) + ":00Z"
            if (int(key[3:]) + 10) >= 60:
                end_time = str(now[:11]) + str(int(key[0:2]) + 1) + ":0" + str(int(key[3:]) + self._timePerTask - 60) + ":00Z"
            else:
                end_time = str(now[:11]) + str(key[0:3]) + str(int(key[3:]) + self._timePerTask) + ":00Z"
            event = {
                'summary': str(value),
                'location': 'Lincoln, UK',
                'description': str(value),
                'start': {
                    'dateTime': now,
                    'timeZone': 'GMT+01:00',
                },
                "end": {
                    'dateTime': end_time,
                    'timeZone': 'GMT+01:00',
                }
            }
            event = self._service.events().insert(calendarId="primary", body=event).execute()
            print("Event created : %s" % (event.get("htmlLink")))
