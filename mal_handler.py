from time import sleep

import requests
import xml.etree.ElementTree as ET
import os

with open(os.path.join(os.path.dirname(__file__), 'password.txt'), "r") as f:
    # the auth token used with the MAL api
    auth = (f.readline().strip(), f.readline().strip())


def search(anime_name):
    """

    :param anime_name: the name of the anime to search on MAL
    :rtype: Anime
    :return: the Anime on MAL with that exact name; ignoring caps.
    """
    global auth
    r = requests.get('https://myanimelist.net/api/anime/search.xml', params={'q': anime_name}, auth=auth)
    if r.status_code is not 200:
        print "Could not complete search. Retrying..."
        sleep(2)
        return search(anime_name)
    found_anime = []
    try:
        root = ET.fromstring(r.content)
        for child in root.findall("entry"):
            id = int(child.find("id").text)
            title = child.find('title').text
            found_anime.append(Anime(id, title))
    except ET.ParseError:
        print "Got invalid data. Was suppose to get data about anime_name, instead got this:"
        print r.content
        raise Exception("Got invalid response from server!")
    try:
        return [a for a in found_anime if a.title.lower() == anime_name.lower()].pop()
    except IndexError:
        print "Cannot find an anime with that title."
        raise Exception("Could not find anime with title %s" % anime_name)


def get_anime_from_list(anime):
    """
    :param anime: The id or Anime class to find
    :rtype: xml.etree.ElementTree.Element
    :return: The xml entry from auther's MAL
    """
    if isinstance(anime, Anime):
        id = anime.id
    else:
        id = anime
    r = requests.get('https://myanimelist.net/malappinfo.php', params={'u': auth[0], 'status': 'all', 'type': 'anime'})
    try:
        root = ET.fromstring(r.content)
    except ET.ParseError:
        print "Got invalid data. Was suppose to get data about anime from your MAL, instead got this:"
        print r.content
        raise Exception("Got invalid response from server!")
    for entry in root.findall('anime'):
        if entry.find('series_animedb_id').text == str(id):
            return entry
    raise Exception("The anime %s is not on your MAL!" % str(anime))


def get_last_completed_episode(anime):
    """

    :param anime: the anime object or anime id to get the last completed episode for
    :return: the number of the last completed episode
    """
    entry = get_anime_from_list(anime)
    return int(entry.find('my_watched_episodes').text) if entry.find('my_watched_episodes').text else 0


def set_last_episode(anime, episode):
    """

    :param anime: the anime object or anime id to change the last completed episode for
    :param episode: the number of the last completed episode to set
    """
    global auth
    if isinstance(anime, Anime):
        id_number = anime.id
    else:
        id_number = anime
    template = ET.parse('/home/thinkredstone/Scripts/Playall/template.xml').getroot()
    template.find('episode').text = str(episode)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(template)
    data = {'data': xml}
    requests.post("https://myanimelist.net/api/animelist/update/%d.xml" % id_number, auth=auth, data=data)


class Anime:
    __doc__ = "this class represents a specific anime on MAL using it's id and title"

    def __init__(self, id, title):
        """

        :param id: the id of the anime
        :param title: the title of the anime
        """
        self.id = id
        self.title = title

    def __repr__(self):
        return "%s (ID: %d)" % (self.title, self.id)


if __name__ == "__main__":
    anime = search('blood lad')
    print get_last_completed_episode(anime)
