#!/usr/bin/env python3
"""
☀️ Wake Up, Justin — 起床曲

A gentle alarm that doesn't want to be hated.

Concept: Most alarms are aggressive. This one earns your attention gradually.
Uses a pentatonic scale (no dissonance, impossible to sound harsh) and builds
from almost-nothing to a melody you'd actually want to hear.

Structure:
  Phase 1 (bars 1-4):   Single notes, widely spaced. Like someone gently
                          tapping your shoulder. C pentatonic, very soft.
                          Just the high register — wind chimes.

  Phase 2 (bars 5-8):   Two notes at a time. A simple pattern emerges.
                          Still soft but now there's rhythm. Your brain
                          starts tracking it even while half-asleep.

  Phase 3 (bars 9-16):  Full melody. Bright, warm, like sunlight through
                          curtains. The melody is in G major pentatonic
                          (shifted up for energy). Steady eighth notes
                          with a singable tune.

  Phase 4 (bars 17-20): The "okay fine I'm up" section. Fuller chords,
                          the melody gets playful — little ornaments,
                          like it's happy you're awake.

Tempo: Starts at 60, accelerates to 100.

Secret: The phase 3 melody spells out G-A-B-D-E = "GABDE" which is
        nonsense but sounds great. Pentatonic can't fail.
"""

from midiutil import MIDIFile
import os

midi = MIDIFile(2)  # melody + accompaniment

# Tempo ramp
midi.addTempo(0, 0, 60)     # Phase 1: sleepy
midi.addTempo(0, 16, 72)    # Phase 2: stirring
midi.addTempo(0, 32, 88)    # Phase 3: awake
midi.addTempo(0, 64, 100)   # Phase 4: up!

for t in range(2):
    midi.addTempo(t, 0, 60)
    midi.addTempo(t, 16, 72)
    midi.addTempo(t, 32, 88)
    midi.addTempo(t, 64, 100)

def n(track, ch, pitch, start, dur, vel):
    midi.addNote(track, ch, pitch, start, dur, vel)

# C pentatonic: C D E G A (no F, no B — no tension)
# G pentatonic: G A B D E

# ============================================================
# PHASE 1: Wind chimes (bars 1-4, beats 0-15)
# Sparse high notes. Like distant bells.
# ============================================================
chimes = [
    (84, 0, 2, 30),      # C6
    (88, 3, 1.5, 28),    # E6
    (91, 6, 2, 32),      # G6
    (84, 10, 1.5, 25),   # C6
    (88, 13, 2, 30),     # E6
]
for p, s, d, v in chimes:
    n(0, 0, p, s, d, v)

# ============================================================
# PHASE 2: Pattern emerging (bars 5-8, beats 16-31)
# Two-note figures. A rhythm your brain can latch onto.
# ============================================================
pattern = [
    # pair 1
    (79, 16, 1, 40),     # G5
    (76, 17, 1, 38),     # E5
    # pair 2
    (79, 20, 1, 42),     # G5
    (74, 21, 1, 40),     # D5
    # pair 3
    (81, 24, 1, 45),     # A5
    (79, 25, 1, 42),     # G5
    # pair 4
    (84, 28, 1, 48),     # C6
    (81, 29, 1.5, 45),   # A5
]
for p, s, d, v in pattern:
    n(0, 0, p, s, d, v)

# Soft bass notes start
n(1, 1, 48, 16, 8, 35)    # C3
n(1, 1, 55, 24, 8, 38)    # G3

# ============================================================
# PHASE 3: The melody (bars 9-16, beats 32-63)
# G major pentatonic. Bright, singable, like a good morning.
# ============================================================

melody = [
    # bar 9-10: theme statement
    (67, 32, 1, 65),      # G4
    (69, 33, 1, 62),      # A4
    (71, 34, 1.5, 68),    # B4
    (74, 36, 1, 70),      # D5
    (76, 37, 2, 72),      # E5
    (74, 39.5, 1, 65),    # D5

    # bar 11-12: answer
    (71, 41, 1, 62),      # B4
    (69, 42, 1.5, 65),    # A4
    (67, 44, 2, 68),      # G4
    (69, 46, 1, 62),      # A4
    (71, 47, 1.5, 65),    # B4

    # bar 13-14: repeat higher, more energy
    (74, 49, 1, 70),      # D5
    (76, 50, 1, 72),      # E5
    (79, 51, 1.5, 75),    # G5
    (76, 53, 1, 70),      # E5
    (74, 54, 1.5, 68),    # D5
    (71, 56, 2, 65),      # B4

    # bar 15-16: landing
    (69, 58, 1, 62),      # A4
    (67, 59, 1.5, 65),    # G4
    (71, 61, 1, 68),      # B4
    (67, 62, 2, 70),      # G4 — home
]

for p, s, d, v in melody:
    n(0, 0, p, s, d, v)

# Accompaniment: arpeggiated chords
accomp_3 = [
    # G chord arpeggio pattern
    (43, 32, 1, 45), (55, 33, 1, 42), (59, 34, 1, 40), (55, 35, 1, 42),
    (43, 36, 1, 45), (55, 37, 1, 42), (59, 38, 1, 40), (55, 39, 1, 42),
    # Em
    (40, 40, 1, 45), (52, 41, 1, 42), (55, 42, 1, 40), (52, 43, 1, 42),
    (40, 44, 1, 45), (52, 45, 1, 42), (55, 46, 1, 40), (52, 47, 1, 42),
    # C
    (48, 48, 1, 45), (55, 49, 1, 42), (60, 50, 1, 40), (55, 51, 1, 42),
    (48, 52, 1, 45), (55, 53, 1, 42), (60, 54, 1, 40), (55, 55, 1, 42),
    # D → G
    (50, 56, 1, 45), (57, 57, 1, 42), (62, 58, 1, 40), (57, 59, 1, 42),
    (43, 60, 1, 48), (55, 61, 1, 45), (59, 62, 1, 42), (55, 63, 1, 42),
]
for p, s, d, v in accomp_3:
    n(1, 1, p, s, d, v)

# ============================================================
# PHASE 4: Playful (bars 17-20, beats 64-79)
# Ornaments, grace notes, the melody is happy you're up
# ============================================================

playful = [
    # Grace note → main note patterns
    (76, 64, 0.25, 60),   # E5 grace
    (74, 64.25, 1, 72),   # D5
    (71, 65.5, 0.5, 68),  # B4
    (74, 66, 1, 72),      # D5
    (76, 67, 0.25, 60),   # E5 grace
    (79, 67.25, 1.5, 75), # G5 — bright!

    (81, 69, 0.25, 65),   # A5 grace
    (79, 69.25, 1, 72),   # G5
    (76, 70.5, 0.5, 68),  # E5
    (74, 71, 1, 70),      # D5

    # Final happy run
    (67, 72, 0.5, 68),    # G4
    (69, 72.5, 0.5, 68),  # A4
    (71, 73, 0.5, 70),    # B4
    (74, 73.5, 0.5, 72),  # D5
    (76, 74, 0.5, 74),    # E5
    (79, 74.5, 0.5, 76),  # G5
    (83, 75, 0.5, 78),    # B5
    (84, 75.5, 3, 80),    # C6 — ding! You're up! ☀️
]

for p, s, d, v in playful:
    n(0, 0, p, s, d, v)

# Full chords for phase 4
n(1, 1, 43, 64, 4, 52)   # G2
n(1, 1, 55, 64, 4, 48)   # G3
n(1, 1, 59, 64, 4, 45)   # B3
n(1, 1, 48, 68, 4, 52)   # C3
n(1, 1, 55, 68, 4, 48)   # G3
n(1, 1, 60, 68, 4, 45)   # C4
n(1, 1, 43, 72, 8, 55)   # G2
n(1, 1, 55, 72, 8, 50)   # G3
n(1, 1, 59, 72, 8, 48)   # B3
n(1, 1, 62, 72, 8, 45)   # D4

out = os.path.expanduser('~/clawspace/melody-experiment/wake-up-justin.mid')
with open(out, 'wb') as f:
    midi.writeFile(f)
print(f"☀️ Wrote {out}")
