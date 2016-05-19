#!/usr/bin/python
from os import getcwd
from subprocess import call
from sys import argv
from mal_handler import *


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
    try:
        while True:
            if len(argv) > 1:
                write_anime(' '.join(argv[1:]))
                anime = search(' '.join(argv[1:]))[0]
            else:
                anime = search(read_anime())[0]
            print anime
            episode = get_last_episode(anime)
            print episode
            command = raw_input("Enter command\n")
            if "p" in command:
                play_episode(episode + 1)
            if "n" in command:
                set_last_episode(anime, episode + 1)
                episode += 1
                play_episode(episode + 1)
            if "c" in command:
                set_last_episode(episode)
                break
    except (KeyboardInterrupt, SystemExit):
        pass
