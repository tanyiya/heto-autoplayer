import json

def parse_score(score_str):
    events = []
    i = 0
    length = len(score_str)

    while i < length:
        chord=[]
        duration = 1
        dot_count = 0
        if score_str[i] not in "[]01234567^_-.":
            print("未知符號:", score_str[i])
            i+=1
        # 判斷 chord
        if score_str[i] == "[":
            i += 1
            while i < length and score_str[i] != "]":
                if score_str[i] in "1234567":
                    note = score_str[i]
                    i += 1
                    if i < length and score_str[i] in "^_":
                        note += score_str[i]
                        i += 1
                    chord.append(note)
                else:
                    i += 1
            i += 1  # 跳過 ]
        elif score_str[i] in "01234567-":
            note = score_str[i]
            i += 1
            if i < length and score_str[i] in "^_":
                note += score_str[i]
                i += 1
                if i < length and score_str[i] in "^":
                    note += score_str[i]
                    i += 1

            if note != "0":
                chord=[note]
        
        
        # 延長符號 '-'
        while i < length and score_str[i] == ".":
            dot_count += 1
            i += 1
        if dot_count != 0:
            t=0.5**dot_count
            duration = duration-1+t

        events.append((chord, duration))
    
    new_events = []

    for chord, duration in events:
        if chord == ["-"]:
            if new_events:
                prev_chord, prev_duration = new_events[-1]
                new_events[-1] = (prev_chord, prev_duration + duration)
        else:
            new_events.append((chord, duration))
    
    return new_events

def compile(song):
    song_data = json.load(open("song.json", "r", encoding="utf-8"))
    music = song_data["songs"][int(song)-1]
    print(f"{music['title']} 編譯中")

    parsed = {
        "left_hand": parse_score("".join(music["left_hand"])),
        "right_hand": parse_score("".join(music.get("right_hand", []))),
        "third_hand": parse_score("".join(music.get("third_hand", [])))
    }
    print(f"{music['title']}編譯完成")

    with open("parsed.json", "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=4)
    print("儲存編譯結果")
    