#!/usr/bin/env python
from __future__ import print_function
import httplib2
import os
from os import path
import json
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
APPLICATION_NAME = 'Menu Grabber'


def get_credentials():
    mydir = path.dirname(__file__)
    secrets_path = path.join(mydir, "google_secrets.json")

    credential_path = os.path.join(mydir,
                                   'sheets_grabber_tokenstore.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(secrets_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

class SheetDataManager(object):
    SHEET_ID = '1nvgTvk20O6rUyY46JkzcyUi7cVmb4sPPA7DiLosVTbg'

    def __init__(self):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
            'version=v4')
        self._service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    # This is meant to find *some* set of date ranges from the names in the sheets.
    # The result is a dict of sheetId: {title: title, start: start_date, end: end_date}
    # End is the saturday date to test for date rangeiness (midnight saturday morning => eow)
    def parse_all_date_ranges(self):
        api_result = self._service.spreadsheets().get(spreadsheetId=SheetDataManager.SHEET_ID).execute()
        # Abbreviate this a bit.
        dt = datetime.datetime
        data = []
        for sheet in api_result['sheets']:
            title = sheet["properties"]["title"]
            # Assumption 1: can split on hyphen. Don't consider those we can't, like "Template"
            if title == u'Template': continue
            (start_str, end_str) = [str.strip() for str in title.split('-')]
            # Assume it's the same year. Will vary over year boundaries, but I don't care yet until it breaks :grin:
            start = dt.strptime(start_str, "%b %d").replace(year=dt.today().year)
            end = dt.strptime(end_str, "%b %d").replace(year=dt.today().year) + datetime.timedelta(days=1)
            row = {}
            row["title"] = sheet["properties"]["title"]
            row["start"] = start
            row["end"] = end
            row["sheetId"] = sheet["properties"]["sheetId"]
            data.append(row)
        return data

    def current_sheet(self):
        current_date = datetime.datetime.today()
        for sheetdata in self.parse_all_date_ranges():
            if current_date > sheetdata["start"] and current_date < sheetdata["end"]:
                return sheetdata["title"]
        return "NOT FOUND"
        

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """


    sheet = SheetDataManager()
    date_ranges = sheet.parse_all_date_ranges()
    print(date_ranges)
    print(sheet.current_sheet())
    
    #rangeName = 'Feb 5-Feb 9!B3:F52'
    #result = service.spreadsheets().values().get(
    #    spreadsheetId=spreadsheetId, range=rangeName).execute()
    #values = result.get('values', [])

    #if not values:
    #    print('No data found.')
    #else:
    #    for row in values:
    #        print(row)


if __name__ == '__main__':
    main()

