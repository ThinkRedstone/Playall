#!/usr/bin/python
from getopt import gnu_getopt
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
        options, name = gnu_getopt(argv[1:], '-r')
        if len(name) > 0:
            write_anime(' '.join(name))
            anime = search(' '.join(name))[0]
        else:
            anime = search(read_anime())[0]
        if [(o, v) for o, v in options if o == '-r']:
            rewatching = True
        else:
            rewatching = False
        current_episode = get_last_completed_episode(anime, rewatching=rewatching) + 1
        while True:
            print anime
            print current_episode
            command = raw_input("Enter command\n")
            if "p" in command:
                play_episode(current_episode)
            if "n" in command:
                set_last_episode(anime, current_episode)
                current_episode += 1
                play_episode(current_episode)
            if "c" in command:
                set_last_episode(anime, current_episode)
                break
    except (KeyboardInterrupt, SystemExit):
        pass
