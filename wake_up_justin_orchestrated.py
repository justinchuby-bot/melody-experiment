#!/usr/bin/env python3
"""
☀️ Wake Up, Justin — 起床曲 [配器版]

配器方案与理由：
  - Phase 1: 钟琴 (GM #9) — 风铃/远处的钟声。原版描述的就是 wind chimes，
    钟琴是完美的对应。每个音符像晨光中的一个光点。
  - Phase 2: 马林巴 (GM #12) — 木质温暖。从金属（钟琴）过渡到木头（马林巴），
    像从梦境走向现实。马林巴有节奏感但不aggressive。
  - Phase 3 melody: 木吉他 (GM #25, Steel Guitar) — 旋律主体。吉他的拨弦声
    像有人在你床边轻轻弹琴叫你起床。配合弦乐伴奏。
  - Phase 3 accomp: 弦乐合奏 (GM #48) — 温暖的地毯。琶音伴奏用弦乐来铺，
    给吉他旋律一个柔软的背景。
  - Phase 4: 弦乐齐奏 (GM #48) + 钟琴回归 — 完整旋律，所有人都醒了。
    钟琴在最后的上行音阶回来，像太阳完全升起。
  - 全程: 大提琴 (GM #42) — 低音线。温暖、稳定、像被窝的安全感。

发现：渐进式配器（金属→木→弦→齐奏）和原版的渐进式力度+速度变化形成了
双重渐强——不只是音量在增加，色彩也在丰富。这让"起床"的叙事更有说服力。
"""

from midiutil import MIDIFile
import os

midi = MIDIFile(6)  # glockenspiel, marimba, guitar, strings, cello-bass, glock-return

# Tempo ramp
tempos = [(0, 60), (16, 72), (32, 88), (64, 100)]
for t in range(6):
    for beat, bpm in tempos:
        midi.addTempo(t, beat, bpm)

# Program changes
midi.addProgramChange(0, 0, 0, 9)    # Glockenspiel (Phase 1)
midi.addProgramChange(1, 1, 0, 12)   # Marimba (Phase 2)
midi.addProgramChange(2, 2, 0, 25)   # Steel Guitar (Phase 3 melody)
midi.addProgramChange(3, 3, 0, 48)   # String Ensemble (Phase 3 accomp + Phase 4)
midi.addProgramChange(4, 4, 0, 42)   # Cello (bass throughout)
midi.addProgramChange(5, 5, 0, 9)    # Glockenspiel (Phase 4 return)

def n(track, ch, pitch, start, dur, vel):
    midi.addNote(track, ch, pitch, start, dur, vel)

# ============================================================
# PHASE 1: Glockenspiel wind chimes (beats 0-15)
# ============================================================
chimes = [
    (84, 0, 2, 32), (88, 3, 1.5, 30), (91, 6, 2, 34),
    (84, 10, 1.5, 27), (88, 13, 2, 32),
]
for p, s, d, v in chimes:
    n(0, 0, p, s, d, v)

# ============================================================
# PHASE 2: Marimba pattern (beats 16-31)
# ============================================================
pattern = [
    (79, 16, 1, 42), (76, 17, 1, 40),
    (79, 20, 1, 44), (74, 21, 1, 42),
    (81, 24, 1, 47), (79, 25, 1, 44),
    (84, 28, 1, 50), (81, 29, 1.5, 47),
]
for p, s, d, v in pattern:
    n(1, 1, p, s, d, v)

# Cello bass enters in Phase 2
n(4, 4, 48, 16, 8, 35)    # C3
n(4, 4, 55, 24, 8, 38)    # G3

# ============================================================
# PHASE 3: Guitar melody + String accomp (beats 32-63)
# ============================================================
melody = [
    (67, 32, 1, 65), (69, 33, 1, 62), (71, 34, 1.5, 68),
    (74, 36, 1, 70), (76, 37, 2, 72), (74, 39.5, 1, 65),
    (71, 41, 1, 62), (69, 42, 1.5, 65), (67, 44, 2, 68),
    (69, 46, 1, 62), (71, 47, 1.5, 65),
    (74, 49, 1, 70), (76, 50, 1, 72), (79, 51, 1.5, 75),
    (76, 53, 1, 70), (74, 54, 1.5, 68), (71, 56, 2, 65),
    (69, 58, 1, 62), (67, 59, 1.5, 65), (71, 61, 1, 68),
    (67, 62, 2, 70),
]
for p, s, d, v in melody:
    n(2, 2, p, s, d, v)

# String ensemble arpeggio accompaniment
accomp = [
    (43, 32, 1, 42), (55, 33, 1, 38), (59, 34, 1, 36), (55, 35, 1, 38),
    (43, 36, 1, 42), (55, 37, 1, 38), (59, 38, 1, 36), (55, 39, 1, 38),
    (40, 40, 1, 42), (52, 41, 1, 38), (55, 42, 1, 36), (52, 43, 1, 38),
    (40, 44, 1, 42), (52, 45, 1, 38), (55, 46, 1, 36), (52, 47, 1, 38),
    (48, 48, 1, 42), (55, 49, 1, 38), (60, 50, 1, 36), (55, 51, 1, 38),
    (48, 52, 1, 42), (55, 53, 1, 38), (60, 54, 1, 36), (55, 55, 1, 38),
    (50, 56, 1, 42), (57, 57, 1, 38), (62, 58, 1, 36), (57, 59, 1, 38),
    (43, 60, 1, 45), (55, 61, 1, 42), (59, 62, 1, 38), (55, 63, 1, 38),
]
for p, s, d, v in accomp:
    n(3, 3, p, s, d, v)

# Cello bass for Phase 3
bass_3 = [
    (43, 32, 8, 45), (40, 40, 8, 45), (48, 48, 8, 45), (43, 56, 8, 48),
]
for p, s, d, v in bass_3:
    n(4, 4, p, s, d, v)

# ============================================================
# PHASE 4: Full ensemble — strings + glockenspiel return (beats 64-79)
# ============================================================
playful = [
    (76, 64, 0.25, 62), (74, 64.25, 1, 72), (71, 65.5, 0.5, 68),
    (74, 66, 1, 72), (76, 67, 0.25, 62), (79, 67.25, 1.5, 75),
    (81, 69, 0.25, 67), (79, 69.25, 1, 72), (76, 70.5, 0.5, 68),
    (74, 71, 1, 70),
    (67, 72, 0.5, 68), (69, 72.5, 0.5, 68), (71, 73, 0.5, 70),
    (74, 73.5, 0.5, 72), (76, 74, 0.5, 74), (79, 74.5, 0.5, 76),
    (83, 75, 0.5, 78), (84, 75.5, 3, 80),
]

# Strings play the melody in Phase 4
for p, s, d, v in playful:
    n(3, 3, p, s, d, v)

# Glockenspiel returns for the final ascending run
final_glock = [
    (79, 72, 0.5, 55), (81, 72.5, 0.5, 57), (83, 73, 0.5, 60),
    (86, 73.5, 0.5, 62), (88, 74, 0.5, 65), (91, 74.5, 0.5, 68),
    (95, 75, 0.5, 70), (96, 75.5, 4, 72),  # C7 — sunrise!
]
for p, s, d, v in final_glock:
    n(5, 5, p, s, d, v)

# String chords Phase 4
n(3, 3, 43, 64, 4, 52)
n(3, 3, 55, 64, 4, 48)
n(3, 3, 59, 64, 4, 45)
n(3, 3, 48, 68, 4, 52)
n(3, 3, 55, 68, 4, 48)
n(3, 3, 60, 68, 4, 45)

# Final chord — full, bright
n(4, 4, 43, 72, 8, 55)    # G2 cello
n(3, 3, 55, 72, 8, 50)    # G3
n(3, 3, 59, 72, 8, 48)    # B3
n(3, 3, 62, 72, 8, 45)    # D4

out = os.path.expanduser('~/clawspace/melody-experiment/wake-up-justin-orchestrated.mid')
with open(out, 'wb') as f:
    midi.writeFile(f)
print(f"☀️ Wrote {out}")
