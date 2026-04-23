"""
实验1: Canon (对位法) — Claw 🦞
=================================
在试什么：写一首真正的三声部卡农。
- 主题：8小节，C大调，4/4拍
- 声部1 (Violin I): 从头开始
- 声部2 (Violin II): 延迟2小节，完全模仿
- 声部3 (Cello): 延迟4小节，低八度完全模仿

为什么：卡农是对位法最纯粹的形式——同一个旋律在时间和音高上错开，
产生和声。三声部+低八度让织体更丰满。

发现：当主题设计得好（避免和声冲突），三个声部叠加后自然形成
I-V-vi-IV等和弦进行。低八度大提琴给了整体一个温暖的根基。
"""

from midiutil import MIDIFile

midi = MIDIFile(3)  # 3 tracks

# Setup
tempo = 72
for i, name in enumerate(["Violin I", "Violin II", "Cello"]):
    midi.addTrackName(i, 0, name)
    midi.addTempo(i, 0, tempo)

# GM instruments: 40=Violin, 42=Cello
midi.addProgramChange(0, 0, 0, 40)  # Violin
midi.addProgramChange(1, 1, 0, 40)  # Violin
midi.addProgramChange(2, 2, 0, 42)  # Cello

# 主题: 8小节 (32拍), C大调
# 每个元素: (pitch_MIDI, duration_in_beats)
theme = [
    # Bar 1
    (72, 1), (74, 1), (76, 1), (77, 1),
    # Bar 2
    (79, 2), (76, 2),
    # Bar 3
    (74, 1), (72, 1), (71, 1), (72, 1),
    # Bar 4
    (74, 2), (67, 2),
    # Bar 5
    (69, 1), (71, 1), (72, 1), (74, 1),
    # Bar 6
    (76, 1.5), (74, 0.5), (72, 2),
    # Bar 7
    (71, 1), (69, 1), (67, 1), (69, 1),
    # Bar 8
    (72, 3), (0, 1),  # 0 = rest (we'll skip it)
]

def add_theme(track, channel, start_beat, octave_shift=0):
    t = start_beat
    for pitch, dur in theme:
        if pitch > 0:
            midi.addNote(track, channel, pitch + octave_shift, t, dur, 80)
        t += dur

# Voice 1: Violin I, starts at beat 0
add_theme(0, 0, 0)
# Voice 2: Violin II, starts at beat 8 (2 bars)
add_theme(1, 1, 8)
# Voice 3: Cello, starts at beat 16 (4 bars), one octave lower
add_theme(2, 2, 16, octave_shift=-12)

# Add a sustained tonic at the end for resolution
end_beat = 16 + 32  # after cello finishes
for track, ch, pitch in [(0, 0, 72), (1, 1, 76), (2, 2, 60)]:
    midi.addNote(track, ch, pitch, end_beat, 4, 70)

with open("canon_experiment.mid", "wb") as f:
    midi.writeFile(f)

print("✅ canon_experiment.mid generated")
