import mido
import json
import os
import math

NOTE_TO_MIDI = {
    "1_": 48, "1_/": 49, "2_": 50, "2_/": 51, "3_": 52, "4_": 53, "4_/": 54, "5_": 55, "5_/": 56, "6_": 57, "6_/": 58, "7_": 59,
    "1": 60, "1/": 61, "2": 62, "2/": 63, "3": 64, "4": 65, "4/": 66, "5": 67, "5/": 68, "6": 69, "6/": 70, "7": 71,
    "1^": 72, "1^/": 73, "2^": 74, "2^/": 75, "3^": 76, "4^": 77, "4^/": 78, "5^": 79, "5^/": 80, "6^": 81, "6^/": 82, "7^": 83, "1^^": 84
}

MIDI_TO_NOTE = {v: k for k, v in NOTE_TO_MIDI.items()}


def beats_to_symbols(beats):
    result = ""

    # long rests
    while beats >= 1:
        result += "0---"
        beats -= 1

    # half beat
    if beats >= 0.5:
        result += "0."
        beats -= 0.5

    # quarter beat
    if beats >= 0.25:
        result += "0.."
        beats -= 0.25

    return result


def midi_to_heto(midi_path, output_name="converted_song"):
    try:
        mid = mido.MidiFile(midi_path)
    except Exception as e:
        print(f"Error reading MIDI: {e}")
        return

    bpm = 120
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                bpm = mido.tempo2bpm(msg.tempo)
                break

    playable_tracks = [t for t in mid.tracks if any(getattr(m, 'type', None) == 'note_on' for m in t)]

    hands_data = {"right_hand": [], "left_hand": []}
    hand_labels = ["right_hand", "left_hand"]

    for idx, track in enumerate(playable_tracks):
        if idx >= 2:
            break

        current_hand = hand_labels[idx]
        ticks_per_beat = mid.ticks_per_beat

        abs_ticks = 0
        notes_at_time = {}

        for msg in track:
            abs_ticks += msg.time

            if msg.type == 'note_on' and msg.velocity > 0 and msg.note in MIDI_TO_NOTE:
                if abs_ticks not in notes_at_time:
                    notes_at_time[abs_ticks] = []
                notes_at_time[abs_ticks].append(MIDI_TO_NOTE[msg.note])

        if not notes_at_time:
            continue

        sorted_times = sorted(notes_at_time.keys())

        score_chunks = []
        current_str = ""

        for i in range(len(sorted_times)):
            t_current = sorted_times[i]
            notes = notes_at_time[t_current]

            note_part = f"[{''.join(notes)}]" if len(notes) > 1 else notes[0]

            current_str += note_part

            if i < len(sorted_times) - 1:
                t_next = sorted_times[i + 1]
                gap_beats = (t_next - t_current) / ticks_per_beat

                # subtract the base beat the note already occupies
                remaining_gap = gap_beats - 1

                if remaining_gap > 0:
                    rest_symbols = beats_to_symbols(remaining_gap)
                    current_str += rest_symbols
                else:
                    # shorter durations use dots (original behaviour preserved)
                    if gap_beats < 1:
                        dot_count = round(math.log(gap_beats, 0.5))
                        dot_count = max(1, min(dot_count, 6))
                        current_str += "." * dot_count

            if len(current_str) > 20:
                score_chunks.append(current_str)
                current_str = ""

        if current_str:
            score_chunks.append(current_str)

        hands_data[current_hand] = score_chunks

    output_json = {
        "songs": [{
            "title": output_name,
            "BPM": int(bpm),
            "hand": "雙手",
            "instrument": "halftone-on",
            "left_hand": hands_data["left_hand"] if hands_data["left_hand"] else (
                hands_data["right_hand"] if hands_data["right_hand"] else []
            ),
            "right_hand": hands_data["right_hand"] if hands_data["left_hand"] else [],
            "third_hand": []
        }]
    }

    with open(f"{output_name}.json", "w", encoding="utf-8") as f:
        json.dump(output_json, f, ensure_ascii=False, indent=4)

    print(f"Successfully converted to {output_name}.json")


if __name__ == "__main__":
    path = input("Enter MIDI path: ").strip('"')
    if os.path.exists(path):
        midi_to_heto(path)