import requests
import xml.etree.ElementTree as ET

auth = ("thinkredstone", "***REMOVED***")


def search(anime):
    global auth
    r = requests.get('http://myanimelist.net/api/anime/search.xml', params={'q': anime}, auth=auth)
    if r.status_code is not 200:
        raise Exception
    root = ET.fromstring(r.content)
    ret = []
    for child in root.findall("entry"):
        id = int(child.find("id").text)
        title = child.find('title').text
        ret.append(Anime(id, title))
    return ret


class Anime:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __repr__(self):
        return "%s (ID: %d)" % (self.title, self.id)
