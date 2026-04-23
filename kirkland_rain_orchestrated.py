#!/usr/bin/env python3
"""
🌧️ Kirkland Rain Morning — 柯克兰的雨天早晨 [配器版]

配器方案与理由：
  - Track 0: 长笛 (GM #73) — 雨滴。原版用高音区钢琴模拟雨滴，长笛的气息感
    更像真实的雨——每一滴都有呼吸。长笛的泛音在高音区天然通透，不需要用力。
  - Track 1: 钢琴 (GM #0) — 主旋律。这首曲子本质是"你在雨天醒来"的内心独白，
    钢琴最适合表达这种私密的、自言自语般的旋律。
  - Track 2: 大提琴 (GM #42) — 和声底层。原版的左手和弦用大提琴来承担，
    温暖的低音弦乐给雨天加了一层"被子"的感觉——你裹着毯子听雨。
  - Track 3: 双簧管 (GM #68) — Section B 的对旋律。咖啡段落加入双簧管，
    它的音色有一种"鼻腔共鸣"的温暖，像厨房里飘来的香气。
  - Track 4 (ch 9): 轻柔打击乐 — 用 MIDI 鼓组的 closed hi-hat 和 ride cymbal
    模拟雨打窗户的节奏，非常轻。

发现：配器之后雨声和旋律的层次感完全不同了。原版是一架钢琴在讲所有的事，
配器版是一个小房间里的几个声音在各自呢喃——但说的是同一件事。
"""

from midiutil import MIDIFile
import os, random

random.seed(2026)

midi = MIDIFile(5)  # flute-rain, piano-melody, cello-chords, oboe-counter, percussion
TEMPO = 72

for t in range(5):
    midi.addTempo(t, 0, TEMPO)

# Program changes
midi.addProgramChange(0, 0, 0, 73)   # Flute
midi.addProgramChange(1, 1, 0, 0)    # Piano
midi.addProgramChange(2, 2, 0, 42)   # Cello
midi.addProgramChange(3, 3, 0, 68)   # Oboe

# Track 4 uses channel 9 (drums) — no program change needed

# ============================================================
# RAIN — Flute (Track 0, ch 0)
# ============================================================
rain_notes_dorian = [86, 84, 81, 79, 77]
rain_notes_lydian = [89, 88, 86, 84, 81]

def write_rain(start_beat, bars, note_pool, base_vel=35):
    for i in range(bars * 8):
        t = start_beat + i * 0.5
        pitch = random.choice(note_pool)
        vel = base_vel + random.randint(-8, 12)
        if random.random() < 0.15:
            continue
        midi.addNote(0, 0, pitch, t, 0.4, vel)

write_rain(0, 8, rain_notes_dorian, 33)
write_rain(32, 8, rain_notes_lydian, 28)
write_rain(64, 8, rain_notes_dorian, 30)
write_rain(96, 4, rain_notes_dorian, 22)

# ============================================================
# PERCUSSION — Rain on window (Track 4, ch 9)
# Hi-hat (42) and ride bell (53), very soft
# ============================================================
def write_rain_perc(start_beat, bars, base_vel=18):
    for i in range(bars * 4):  # quarter note grid
        t = start_beat + i * 1.0
        if random.random() < 0.3:
            continue
        # Alternate hi-hat and ride
        drum = 42 if random.random() < 0.7 else 53
        vel = base_vel + random.randint(-5, 8)
        midi.addNote(4, 9, drum, t, 0.3, max(10, vel))

write_rain_perc(0, 8, 18)
write_rain_perc(32, 8, 14)
write_rain_perc(64, 8, 16)
write_rain_perc(96, 4, 10)

# ============================================================
# CELLO — Harmonic foundation (Track 2, ch 2)
# ============================================================
bass_a = [
    ([50, 53, 57], 8),
    ([48, 52, 57], 8),
    ([46, 50, 53], 8),
    ([48, 52, 55], 8),
]
bass_b = [
    ([53, 57, 60, 64], 8),
    ([55, 59, 62], 8),
    ([57, 60, 64], 8),
    ([53, 57, 60, 64], 8),
]
bass_coda = [([50, 53, 57, 60, 64], 16)]

def write_chords(start, chord_list, vel=50):
    t = start
    for notes, dur in chord_list:
        for n in notes:
            midi.addNote(2, 2, n, t, dur, vel)
        t += dur

write_chords(0, bass_a, 48)
write_chords(32, bass_b, 45)
write_chords(64, bass_a, 42)
write_chords(96, bass_coda, 35)

# ============================================================
# PIANO — Melody (Track 1, ch 1)
# ============================================================
melody_a = [
    (62, 0, 3, 55), (64, 4, 2, 50), (65, 7, 3, 55),
    (67, 12, 2, 60), (69, 14.5, 1.5, 58), (67, 16, 4, 55),
    (69, 22, 2, 62), (72, 24, 3, 65), (71, 28, 2, 58),
    (69, 30, 2, 60), (67, 30, 2, 55),
]
melody_b = [
    (65, 32, 1.5, 65), (67, 33.5, 1, 62), (69, 35, 1.5, 68),
    (71, 37, 2, 70), (72, 39.5, 2, 68),
    (74, 42, 1, 65), (72, 43, 1, 62), (71, 44.5, 1.5, 68),
    (69, 46, 2, 65), (72, 47.5, 2, 62),
    (74, 50, 2, 70), (76, 52, 1.5, 72), (74, 54, 1, 65),
    (72, 55.5, 2.5, 68),
    (71, 58, 1.5, 65), (69, 60, 2, 62), (65, 62, 2, 58),
]
melody_a2 = [
    (74, 64, 2, 62), (76, 66.5, 1.5, 60), (77, 68, 3, 65),
    (79, 72, 2, 68), (81, 74, 1.5, 65), (79, 76, 3, 60),
    (81, 80, 2, 68), (84, 82, 2.5, 72), (83, 85, 1.5, 62),
    (81, 87, 2, 60), (79, 89, 2, 55), (74, 92, 3, 50),
]
melody_coda = [
    (62, 96, 6, 45), (65, 103, 8, 30),
]

def write_melody(notes):
    for pitch, start, dur, vel in notes:
        midi.addNote(1, 1, pitch, start, dur, vel)

write_melody(melody_a)
write_melody(melody_b)
write_melody(melody_a2)
write_melody(melody_coda)

# ============================================================
# OBOE — Counter-melody in Section B (Track 3, ch 3)
# Adds warmth during the coffee section, like aroma drifting in
# ============================================================
oboe_b = [
    (60, 34, 3, 50),     # C4
    (62, 38, 2, 52),     # D4
    (64, 41, 2.5, 55),   # E4
    (65, 44, 3, 52),     # F4
    (67, 48, 2, 58),     # G4
    (69, 51, 2, 55),     # A4
    (67, 54, 3, 52),     # G4
    (65, 58, 2, 48),     # F4
    (64, 61, 3, 45),     # E4 — fading as coffee section ends
]
for p, s, d, v in oboe_b:
    midi.addNote(3, 3, p, s, d, v)

# Oboe returns in coda, very soft, a single held note
midi.addNote(3, 3, 62, 100, 10, 25)  # D4 — like a sigh

# Write
out = os.path.expanduser('~/clawspace/melody-experiment/kirkland-rain-orchestrated.mid')
with open(out, 'wb') as f:
    midi.writeFile(f)
print(f"🌧️ Wrote {out}")
