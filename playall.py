#!/usr/bin/python2
from os import getcwd
from subprocess import call
from mal_handler import *
from threading import Thread
import argparse
import os

ROOT_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
SCRIPT_PATH = os.path.join(ROOT_DIR, "play_episode.sh")


def episode_string(n):
    return str(n / 10) + str(n % 10)


def read_anime(directory=getcwd()):
    with open(directory + "/.playall", "r") as f:
        return f.readline()


def write_anime(anime, directory=getcwd()):
    with open(directory + "/.playall", "w+") as f:
        f.write(str(anime))


def play_episode(episode, directory=getcwd()):
    try:
        call('%s "%s" %s' % (SCRIPT_PATH, directory, episode_string(episode)), shell=True)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('anime_name', nargs='?', help="Anime name to search on MAL (Exact Spelling)")
    parser.add_argument("-d", "--directory", default=getcwd(), help="Directory to run playall from (default is cwd)")
    args = parser.parse_args()
    directory = os.path.abspath(args.directory) + "/"
    try:
        anime_name = read_anime(directory=directory)
    except IOError:
        anime_name = args.anime_name
        write_anime(anime_name, directory=directory)
    anime = [a for a in search(anime_name) if a.title.lower() == anime_name.lower()].pop()
    current_episode = get_last_completed_episode(anime) + 1
    try:
        while True:
            print anime
            print current_episode
            command = raw_input("Enter command\n")
            if "p" in command:
                play_episode(current_episode, directory=directory)
            if "n" in command:
                Thread(target=set_last_episode, args=(anime, current_episode)).start()
                current_episode += 1
                play_episode(current_episode, directory=directory)
            if "c" in command:
                set_last_episode(anime, current_episode)
                break
    except (KeyboardInterrupt, SystemExit):
        pass
