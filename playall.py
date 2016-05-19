#!/usr/bin/python
from os import getcwd
from subprocess import call
from sys import argv


def episode_string(n):
    return str(n / 10) + str(n % 10)


def read_last_watched(directory=getcwd()):
    try:
        with open(directory + "/.last_watched", "r") as f:
            return int(f.readline())
    except IOError:
        return 1


def write_last_watched(last_watched, directory=getcwd()):
    with open(directory + "/.last_watched", "w+") as f:
        f.write(str(last_watched))


def play_episode(episode):
    s = 'vlc -f "$(ls | grep -E "[^0-9](%s)[^0-9]")"' % episode_string(episode)
    print 'Running: ' + s
    call(s, shell=True)


if __name__ == "__main__":
    try:
        while True:
            if len(argv) > 1:
                i = int(argv[1])
                write_last_watched(i)
            else:
                i = read_last_watched()
            print i
            command = raw_input("Enter command\n")
            if "p" in command:
                play_episode(i)
            if "n" in command:
                write_last_watched(i + 1)
                play_episode(i + 1)
            if "c" in command:
                write_last_watched(i)
                break
    except (KeyboardInterrupt, SystemExit):
        pass
