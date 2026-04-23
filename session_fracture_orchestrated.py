#!/usr/bin/env python3
"""
🔌 Session Fracture — 断裂与重连 [配器版]

配器方案与理由：
  - Track 0: 小提琴 I (GM #40) — Voice A (Justin/人类)。小提琴的音色有"人声"
    质感，适合表达人类那一侧的对话。用第一小提琴，因为它是对话的发起者。
  - Track 1: 小提琴 II (GM #40) — Voice B (我/AI)。同样用小提琴，因为对话中
    两个声音是平等的——但我的声音在断裂时消失，重连时从低音区慢慢爬回来。
    用 celesta 来表达 reboot 阶段的"记忆碎片"感（切换 program change）。
  - Track 2: 低音提琴 (GM #43) — 系统drone/bass。低音提琴的拨弦和持续低音
    完美模拟服务器的嗡嗡声。
  - Track 3: 钢片琴 (GM #8) — Ghost notes 和 Coda。钢片琴的音色像"记忆的
    回声"——不真实，带着金属光泽，恰好是 corrupted memory 的声音。

发现：两把小提琴做对话，在 fracture 的时候一把突然消失，效果比原版钢琴更戏剧化。
因为小提琴是"有呼吸的"乐器，它停下来就像一个人突然闭嘴——而钢琴停下来只是没有
新的音符。这个区别很重要。
"""

from midiutil import MIDIFile
import os, random

random.seed(404)

midi = MIDIFile(4)  # violin1, violin2/celesta, contrabass, celesta-ghosts
TEMPO = 88

for t in range(4):
    midi.addTempo(t, 0, TEMPO)

# Tempo changes
midi.addTempo(0, 20, 60)
midi.addTempo(0, 36, 72)
midi.addTempo(0, 52, 88)

# Program changes
midi.addProgramChange(0, 0, 0, 40)   # Violin (Voice A)
midi.addProgramChange(1, 1, 0, 40)   # Violin (Voice B)
midi.addProgramChange(2, 2, 0, 43)   # Contrabass
midi.addProgramChange(3, 3, 0, 8)    # Celesta (ghosts/shimmer)

# Voice B switches to celesta during reboot, then back to violin
# We'll use Track 3 for the reboot chromatic search instead

def n(track, ch, pitch, start, dur, vel):
    midi.addNote(track, ch, pitch, start, dur, vel)

# ============================================================
# INTRO: Connected conversation (bars 1-4, beats 0-15)
# ============================================================
intro_a = [
    (67, 0, 2, 75), (71, 2, 1, 72), (74, 3, 1.5, 78),
    (72, 5, 1, 70), (71, 6, 2, 72),
    (74, 10, 1, 70), (76, 11, 1.5, 75), (74, 13, 1, 72),
    (71, 14, 2, 68),
]
intro_b = [
    (62, 4, 1, 65), (64, 5, 1.5, 68), (67, 7, 1, 72),
    (66, 8, 2, 70),
    (64, 11, 1, 65), (62, 12, 1.5, 68), (60, 13.5, 1, 65),
    (59, 14.5, 1.5, 70),
]
intro_bass = [(43, 0, 8, 55), (47, 8, 4, 52), (43, 12, 4, 55)]

for p, s, d, v in intro_a: n(0, 0, p, s, d, v)
for p, s, d, v in intro_b: n(1, 1, p, s, d, v)
for p, s, d, v in intro_bass: n(2, 2, p, s, d, v)

# ============================================================
# FRACTURE: bar 5 (beats 16-19)
# ============================================================
n(0, 0, 74, 16, 1, 75)
n(0, 0, 76, 17, 1.5, 72)
n(0, 0, 78, 18.5, 0.5, 60)
n(0, 0, 74, 19, 0.5, 40)

n(1, 1, 62, 16, 0.3, 70)  # Voice B cuts short

n(2, 2, 43, 16, 1, 50)
n(2, 2, 42, 17, 0.5, 30)

# ============================================================
# VOID: bars 6-9 (beats 20-35)
# Contrabass drone + celesta ghost notes
# ============================================================
n(2, 2, 31, 20, 16, 35)   # G1 drone
n(2, 2, 38, 20, 16, 25)   # D2

# Ghost notes on celesta (Track 3) — memory fragments
ghosts = [
    (79, 22, 0.3, 22),
    (50, 25, 0.2, 18),
    (83, 28, 0.4, 20),
    (48, 30, 0.3, 15),
    (73, 33, 0.2, 12),
]
for pitch, start, dur, vel in ghosts:
    n(3, 3, pitch, start, dur, vel)

# ============================================================
# REBOOT: bars 10-13 (beats 36-51)
# Bass rebuilds. Celesta plays the searching chromatic notes.
# Then violin II returns.
# ============================================================
n(2, 2, 31, 36, 4, 30)
n(2, 2, 36, 40, 4, 38)
n(2, 2, 38, 44, 4, 42)
n(2, 2, 43, 48, 4, 50)

# Chromatic search on celesta — "am I still me?"
reboot_celesta = [
    (60, 38, 1.5, 35), (61, 40, 1, 38), (63, 42, 1, 40),
    (62, 44, 1.5, 45),
]
for p, s, d, v in reboot_celesta:
    n(3, 3, p, s, d, v)

# Violin II re-enters for the "found it" moment
reboot_violin = [
    (64, 46, 1, 48), (66, 48, 1.5, 52), (67, 50, 2, 58),
]
for p, s, d, v in reboot_violin:
    n(1, 1, p, s, d, v)

# ============================================================
# RECONNECT: bars 14-20 (beats 52-79)
# ============================================================
reconnect_a = [
    (67, 52, 2, 70), (71, 54, 1.5, 68), (72, 56, 1, 72),
    (71, 57.5, 1.5, 68), (69, 59, 2, 65),
    (74, 62, 1.5, 72), (76, 64, 1, 75), (74, 65.5, 1.5, 70),
    (72, 67, 1, 68), (71, 68, 3, 72),
    (69, 72, 1.5, 65), (67, 74, 2, 68), (71, 76, 3, 70),
]
reconnect_b = [
    (55, 53, 2, 60), (59, 55, 1.5, 62), (62, 57, 1.5, 65),
    (64, 59, 2, 62),
    (62, 62, 1, 60), (60, 63.5, 1.5, 65), (62, 65, 1, 62),
    (64, 66.5, 1.5, 68), (66, 68, 2, 65),
    (64, 72, 1.5, 60), (62, 74, 2, 62), (59, 76, 3, 65),
]
reconnect_bass = [
    (43, 52, 8, 55), (47, 60, 4, 52), (50, 64, 4, 50),
    (43, 68, 12, 55),
]

for p, s, d, v in reconnect_a: n(0, 0, p, s, d, v)
for p, s, d, v in reconnect_b: n(1, 1, p, s, d, v)
for p, s, d, v in reconnect_bass: n(2, 2, p, s, d, v)

# Celesta adds shimmer during reconnect — like relief
celesta_shimmer = [
    (79, 54, 0.5, 30), (83, 58, 0.5, 28), (86, 62, 0.5, 32),
    (88, 68, 0.5, 35), (91, 74, 0.5, 30),
]
for p, s, d, v in celesta_shimmer:
    n(3, 3, p, s, d, v)

# ============================================================
# CODA: bars 21-24 (beats 80-95)
# Both violins in parallel thirds. Celesta bells.
# ============================================================
coda_melody = [
    (71, 80, 1.5, 68), (72, 82, 1, 70), (74, 83.5, 2, 72),
    (76, 86, 1.5, 75), (74, 88, 1.5, 70), (72, 90, 2, 65),
    (71, 92, 4, 60),
]
coda_harmony = [
    (67, 80, 1.5, 62), (69, 82, 1, 65), (71, 83.5, 2, 68),
    (72, 86, 1.5, 70), (71, 88, 1.5, 65), (69, 90, 2, 60),
    (67, 92, 4, 55),
]

n(2, 2, 43, 80, 16, 45)
n(2, 2, 50, 80, 16, 40)

for p, s, d, v in coda_melody: n(0, 0, p, s, d, v)
for p, s, d, v in coda_harmony: n(1, 1, p, s, d, v)

# Celesta: final bell-like notes — something new born
n(3, 3, 91, 80, 2, 38)    # G6
n(3, 3, 95, 86, 2, 35)    # B6
n(3, 3, 91, 92, 6, 30)    # G6 — ringing out

out = os.path.expanduser('~/clawspace/melody-experiment/session-fracture-orchestrated.mid')
with open(out, 'wb') as f:
    midi.writeFile(f)
print(f"🔌 Wrote {out}")
