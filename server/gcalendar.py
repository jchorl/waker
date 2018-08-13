import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

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
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    end_of_day = datetime.datetime.utcnow() + datetime.timedelta(0, 60 * 60 * 12) # get events for the next 12 hours
    end_of_day = end_of_day.isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        timeMax=end_of_day, maxResults=10,
                                        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    cal_string = 'Here are the upcoming calendar events for today: '
    if not events:
        cal_string = 'There are no calendar events today.'

    all_day_events = [event for event in events if 'dateTime' not in event['start']]
    time_events = [event for event in events if 'dateTime' in event['start']]
    for event in all_day_events:
        cal_string += event['summary'] + '. '
    for event in time_events:
        start = datetime.datetime.fromisoformat(event['start']['dateTime'])
        cal_string += event['summary'] + ' at ' + start.strftime('%H:%M') + '. '
    return cal_string
