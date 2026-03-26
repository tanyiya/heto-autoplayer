import json
import time
import player
import parser

s=1

while s!="0":
    
    json_data = json.load(open("song.json", "r", encoding="utf-8"))
    print("目錄:")
    for idx, song in enumerate(json_data["songs"]):
        print(f"{idx+1}. {song['title']}")
    s = input("選歌:")
    parser.compile(s)
    
    time.sleep(3)
    player.play(s)
    player.start()


