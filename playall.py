#!/usr/bin/python2
from os import getcwd
from subprocess import call
from sys import argv
from mal_handler import *
from threading import Thread
import argparse


def episode_string(n):
    return str(n / 10) + str(n % 10)


def read_anime(directory=getcwd()):
    with open(directory + "/.playall", "r") as f:
        return f.readline()


def write_anime(anime, directory=getcwd()):
    with open(directory + "/.playall", "w+") as f:
        f.write(str(anime))


def play_episode(episode):
    s = 'vlc -f "$(ls | grep -E "[^0-9](%s)[^0-9]")"' % episode_string(episode)
    print 'Running: ' + s
    call(s, shell=True)


if __name__ == "__main__":
    print argv
    parser = argparse.ArgumentParser()
    parser.add_argument('anime_name', nargs='?', help="Anime Name to search on MAL (Exact Spelling)")
    args = parser.parse_args()
    try:
        anime_name = read_anime()
    except IOError:
        anime_name = args.anime_name
        write_anime(anime_name)
    anime = [a for a in search(anime_name) if a.title.lower() == anime_name.lower()].pop()
    current_episode = get_last_completed_episode(anime) + 1
    try:
        while True:
            print anime
            print current_episode
            command = raw_input("Enter command\n")
            if "p" in command:
                play_episode(current_episode)
            if "n" in command:
                Thread(target=set_last_episode, args=(anime, current_episode)).start()
                current_episode += 1
                play_episode(current_episode)
            if "c" in command:
                set_last_episode(anime, current_episode)
                break
    except (KeyboardInterrupt, SystemExit):
        pass
