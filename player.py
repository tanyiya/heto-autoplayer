import threading
import time
import keyboard
import json
import parser


def play_hand(events):

    for chord, duration in events:

        pressed = []

        for note in chord:
            if note in note_map:
                key = note_map[note]
                keyboard.press(key)
                pressed.append(key)

        time.sleep(duration * beat_time)

        for key in pressed:
            keyboard.release(key)


def play(song):

    json_data = json.load(open("song.json", "r", encoding="utf-8"))

    global music
    music = json_data["songs"][int(song)-1]

    global beat_time
    beat_time = 60 / music["BPM"]

    global note_map
    note_map = json.load(open("instrument.json", "r", encoding="utf-8"))[music["instrument"]]


def start():

    song = json.load(open("parsed.json", "r", encoding="utf-8"))

    if music["hand"] == "單手":

        left_hand = song["left_hand"]

        Fthread = threading.Thread(target=play_hand, args=(left_hand,))
        Fthread.start()
        Fthread.join()

    elif music["hand"] == "雙手":

        left_hand = song["left_hand"]
        right_hand = song["right_hand"]
        
        left_total = sum(duration for chord, duration in left_hand)
        right_total = sum(duration for chord, duration in right_hand)

        print("left:", left_total)
        print("right:", right_total)

        Fthread = threading.Thread(target=play_hand, args=(right_hand,))
        Sthread = threading.Thread(target=play_hand, args=(left_hand,))

        Fthread.start()
        Sthread.start()

        Fthread.join()
        Sthread.join()

    else:

        left_hand = song["left_hand"]
        right_hand = song["right_hand"]
        third_hand = song["third_hand"]

        left_total = sum(duration for chord, duration in left_hand)
        right_total = sum(duration for chord, duration in right_hand)
        third_total = sum(duration for chord, duration in third_hand)

        print("left:", left_total)
        print("right:", right_total)
        print("third:",third_total)

        Fthread = threading.Thread(target=play_hand, args=(right_hand,))
        Sthread = threading.Thread(target=play_hand, args=(left_hand,))
        Tthread = threading.Thread(target=play_hand, args=(third_hand,))

        Fthread.start()
        Sthread.start()
        Tthread.start()

        Fthread.join()
        Sthread.join()
        Tthread.join()

    print(f"{music['title']}演奏結束")