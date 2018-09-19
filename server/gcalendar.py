import datetime
import pytz

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from secrets import CALENDARS_TO_CHECK

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def get_calendar_events():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    calendars_result = service.calendarList().list().execute()
    cal_ids = [cal.get('id') for cal in calendars_result.get('items') if cal.get('summary') in CALENDARS_TO_CHECK]

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    end_of_day = datetime.datetime.utcnow() + datetime.timedelta(0, 60 * 60 * 12) # get events for the next 12 hours
    end_of_day = end_of_day.isoformat() + 'Z' # 'Z' indicates UTC time

    all_events = []
    for cal_id in cal_ids:
        events_result = service.events().list(calendarId=cal_id, timeMin=now,
                                            timeMax=end_of_day, maxResults=10,
                                            singleEvents=True, orderBy='startTime').execute()
        all_events.extend(events_result.get('items', []))

    cal_string = 'Here are the upcoming calendar events for today: '
    if not all_events or len(all_events) == 0:
        cal_string = 'There are no calendar events today.'

    all_events.sort(key=get_start_time)
    all_day_events = [event for event in all_events if 'dateTime' not in event['start']]
    time_events = [event for event in all_events if 'dateTime' in event['start']]
    for event in all_day_events:
        cal_string += event['summary'] + '. '
    for event in time_events:
        start = datetime.datetime.fromisoformat(event['start']['dateTime'])
        cal_string += event['summary'] + ' at ' + start.strftime('%H:%M') + '. '
    return cal_string

def get_start_time(event):
    if 'dateTime' in event['start']:
        return datetime.datetime.fromisoformat(event['start']['dateTime']).replace(tzinfo=pytz.UTC)
    return datetime.datetime.fromtimestamp(0).replace(tzinfo=pytz.UTC)

# there is a flag conflict with flask, so running this file standalone will just auth with google
# so the --noauth_local_webserver flag can be passed
if __name__ == '__main__':
    get_calendar_events()
