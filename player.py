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
    # Load the parsed score from the temp file
    song_data = json.load(open("parsed.json", "r", encoding="utf-8"))

    # Fix: Multi-hand detection and assignment
    # We prioritize right_hand if it's a single-hand song and left is empty
    l_hand = song_data.get("left_hand", [])
    r_hand = song_data.get("right_hand", [])
    t_hand = song_data.get("third_hand", [])

    # Logic for Single Hand (單手)
    if music["hand"] == "單手":
        # Use whichever hand actually has data
        active_hand = r_hand if r_hand else l_hand
        Fthread = threading.Thread(target=play_hand, args=(active_hand,))
        Fthread.start()
        Fthread.join()

    # Logic for Two Hands (雙手)
    elif music["hand"] == "雙手":
        # Ensure we don't crash if one hand is missing
        Fthread = threading.Thread(target=play_hand, args=(r_hand,))
        Sthread = threading.Thread(target=play_hand, args=(l_hand,))

        Fthread.start()
        Sthread.start()

        Fthread.join()
        Sthread.join()

    # Logic for Three Hands (三手)
    else:
        Fthread = threading.Thread(target=play_hand, args=(r_hand,))
        Sthread = threading.Thread(target=play_hand, args=(l_hand,))
        Tthread = threading.Thread(target=play_hand, args=(t_hand,))

        Fthread.start()
        Sthread.start()
        Tthread.start()

        Fthread.join()
        Sthread.join()
        Tthread.join()

    print(f"{music['title']} 演奏結束")