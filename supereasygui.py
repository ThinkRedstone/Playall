import easygui
from mal_handler import *
from threading import Thread
from playall import play_episode

anime = easygui.choicebox("Choose anime", "Anime Chooser", sorted(map(lambda a: a.title, search_all(easygui.enterbox()))))
directory = easygui.diropenbox()


def process_input():
    string = easygui.buttonbox("What episode to play?", choices=["Play Next", "Play Current", "Complete and Quit"])
    if string == "Play Next":
        print "playing next"
        return 'n'
    if string == "Play Current":
        print "playing current"
        return 'p'
    if string == "Complete and Quit":
        print "completing"
        return 'c'


anime = search(anime)
current_episode = get_last_completed_episode(anime) + 1
try:
    while True:
        print anime
        print current_episode
        command = process_input()
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
