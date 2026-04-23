"""
实验2: Phase Shift — Steve Reich 风格 Minimalism — Claw 🦞
=========================================================
在试什么：两个声部弹同一个8音循环 pattern，但声部2每次循环
比声部1快一个十六分音符(0.25拍)。从齐奏开始，逐渐错开，
最终在若干循环后重新对齐。

为什么：Steve Reich 的 "Piano Phase" (1967) 证明了最简单的
素材通过相位偏移能产生丰富的节奏和声效果。这是 minimalism 的核心。

发现：8个音的循环需要 8/(0.25) = 32 次循环才能完全重合。
中间过程中产生的"幻影旋律"（两个声部交错形成的新pattern）
是最迷人的部分。用马林巴音色特别适合——泛音衰减快，不会糊。
"""

from midiutil import MIDIFile

midi = MIDIFile(2)
tempo = 120

for i, name in enumerate(["Marimba 1", "Marimba 2"]):
    midi.addTrackName(i, 0, name)
    midi.addTempo(i, 0, tempo)
    midi.addProgramChange(i, i, 0, 12)  # GM 12 = Marimba

# Pattern: 8 notes in E minor pentatonic-ish
pattern_pitches = [64, 66, 67, 69, 71, 72, 71, 69]  # E F# G A B C B A
note_dur = 0.5  # eighth notes
base_cycle = len(pattern_pitches) * note_dur  # 4 beats per cycle

num_cycles = 33  # 32 shifts + 1 to hear reunion
velocity = 85

# Voice 1: constant tempo
t = 0
for cycle in range(num_cycles):
    for p in pattern_pitches:
        midi.addNote(0, 0, p, t, note_dur * 0.9, velocity)
        t += note_dur

# Voice 2: each cycle is 0.25 beats shorter (one sixteenth faster)
shift_per_cycle = 0.25
t2 = 0
for cycle in range(num_cycles):
    cycle_note_dur = note_dur - (shift_per_cycle * (cycle) / len(pattern_pitches))
    # Simpler approach: just shift the start time
    pass

# Actually, cleaner: Voice 2 plays same pattern but each cycle starts
# shift_per_cycle beats earlier relative to voice 1
t2 = 0
for cycle in range(num_cycles):
    effective_dur = note_dur  # keep note duration constant
    for p in pattern_pitches:
        midi.addNote(1, 1, p, t2, effective_dur * 0.9, velocity)
        t2 += effective_dur
    # After each cycle, voice 2 "gains" a sixteenth note
    t2 -= shift_per_cycle

with open("phase_shift.mid", "wb") as f:
    midi.writeFile(f)

print("✅ phase_shift.mid generated")
