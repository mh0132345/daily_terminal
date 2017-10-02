#!/usr/bin/python
from __future__ import print_function
import httplib2
import os
import sys 

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'daily_terminal'

def allCalendars(service):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print (calendar_list_entry['summary'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

def addEvent(service,event_str):
    result = service.events().quickAdd(calendarId='primary', text=event_str, sendNotifications=None).execute()
    listEvents(service,'primary')

def listEvents(service,calenderId):
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('The upcoming 10 events')
    eventsResult = service.events().list(
        calendarId=calenderId, timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        # start = event['start'].get('date')
        start = event['start'].get('dateTime', event['start'].get('date'))
        date = start.split('T')[0]
        time = start.split('T')[1].split('+')[0]
        print(date,"  ",time,"  ", event['summary'])

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def help():
    print("List Upcoming Events : my_calendar upcoming")
    print("Upload a file : my_calendar add <event_string>") 
    print("My VAMK schedule: my_calendar vamk")

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    if len(sys.argv) < 2:
        help()
        
    else:
        option = sys.argv[1]
        if option == "upcoming":
            listEvents(service,'primary')
        elif option == "add":
            event_str = sys.argv[2]
            addEvent(service, event_str)
        elif option == 'vamk':
            listEvents(service, 'al2be12rts2d3hl45hcvo09tdvs1fpc0@import.calendar.google.com')
        elif option == 'month':
            os.system('cal')
        else:
            help()

if __name__ == '__main__':
    main()  