#!/usr/bin/env python

import requests

class BartApi(object):
    API_KEY="MW9S-E7SL-26DU-VV8V"
    URL_ROOT="http://api.bart.gov/api/"

    def __init__(self):
        pass

    def service_advisories(self):
        BartApi.URL_ROOT + "bsa.aspx?cmd=bsa&key=" + BartApi.API_KEY + "&json=y"
        
