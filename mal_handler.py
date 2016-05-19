import requests
import xml.etree.ElementTree as ET

auth = ("thinkredstone", "***REMOVED***")

def search(anime):
    global auth
    r = requests.get('http://myanimelist.net/api/anime/search.xml', params={'q': anime}, auth=auth)
    if r.status_code is not 200:
        raise Exception
    return r.content
