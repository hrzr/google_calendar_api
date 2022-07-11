import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MUSIC_CALENDAR = 'ogit8532b7cim3cll6d8aaqgso@group.calendar.google.com'  # calendar id


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(
            'token.json',
            SCOPES
        )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret_742112645926-kj3sh2rmaeiiquggamn39vajncmm9hmb.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId=MUSIC_CALENDAR, timeMin=now,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
            return
        old_month = 0
        for event in events:
            start = event['start'].get('datetime', event['start'].get('date'))
            month = start.split('-')[1]
            if month != old_month:
                print('---')
                old_month = month
            print(start, event['summary'])
    except HttpError as error:
        print(f"An error occured: {error}")


if __name__ == "__main__":
    main()
