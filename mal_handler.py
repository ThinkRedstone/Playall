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


def get_last_episode(anime):
    if isinstance(anime, Anime):
        id = anime.id
    else:
        id = anime
    r = requests.get('http://myanimelist.net/malappinfo.php', params={'u': auth[0], 'status': 'all', 'type': 'anime'})
    root = ET.fromstring(r.content)
    for entry in root.findall('anime'):
        if entry.find('series_animedb_id').text == str(id):
            return int(entry.find('my_watched_episodes').text)


class Anime:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __repr__(self):
        return "%s (ID: %d)" % (self.title, self.id)


if __name__ == "__main__":
    print get_last_episode(search('boku no hero academia')[0])
