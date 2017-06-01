#!/usr/bin/python2
from os import getcwd
from subprocess import call
from mal_handler import *
from threading import Thread
import argparse
import os

ROOT_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
SCRIPT_PATH = os.path.join(ROOT_DIR, "play_episode.sh")


def episode_string(n, min_length=2):
    s = str(n)
    while len(s) < min_length:
        s = "0" + s
    return s


def read_anime(directory=getcwd()):
    """

    :param directory: the directory containing the .playall file, as generated by @write_anime
    :return: the anime
    """
    with open(directory + "/.playall", "r") as f:
        return search(f.readline())


def write_anime(anime, directory=getcwd()):
    """

    :param anime: the anime class, or a string, to write to the .playall file
    :param directory: the directory in which the .playall file should be generated. Should contain the episodes of that anime.
    """
    with open(directory + "/.playall", "w+") as f:
        f.write(anime.title)


def play_episode(episode, directory=getcwd(), options=""):
    """

    :param episode: the number of the episode to play
    :param directory: the directory containing all the episodes
    :param options: a string containing all the options to be passed to vlc
    """
    options = "" if options is None else " ".join(options)
    try:
        call('%s "%s" %s "%s"' % (SCRIPT_PATH, directory, episode_string(episode), options), shell=True)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('anime', nargs='?', help="Anime name to search on MAL (Exact Spelling)")
    parser.add_argument("-d", "--directory", default=getcwd(), help="Directory to run playall from (default is cwd)")
    parser.add_argument("-o", "--options", nargs="+", help="Extra options to pass to the video player")
    args = parser.parse_args()
    directory = os.path.abspath(args.directory) + "/"
    try:
        anime = search(args.anime) if args.anime else read_anime(directory=directory)
        if anime != read_anime(directory=directory):
            write_anime(anime, directory=directory)
    except IOError:
        anime = search(args.anime)
        write_anime(anime, directory=directory)
    current_episode = get_last_completed_episode(anime) + 1
    try:
        while True:
            print anime
            print current_episode
            command = raw_input("Enter command\n")
            if "p" in command:
                play_episode(current_episode, directory=directory, options=args.options)
            if "n" in command:
                Thread(target=set_last_episode, args=(anime, current_episode)).start()
                current_episode += 1
                play_episode(current_episode, directory=directory, options=args.options)
            if "c" in command:
                set_last_episode(anime, current_episode)
                break
    except (KeyboardInterrupt, SystemExit):
        pass
