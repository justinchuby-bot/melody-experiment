#!/usr/bin/env python3
"""
🌧️ Kirkland Rain Morning — 柯克兰的雨天早晨

A tone poem for a grey Pacific Northwest morning.

Structure:
  A (bars 1-8):   Rain on the window. Sparse, gentle. D dorian mode gives that
                   not-quite-sad, contemplative feeling. The left hand is steady
                   raindrops (repeated eighth-note pattern), the right hand is
                   you slowly waking up — long notes, stretching.

  B (bars 9-16):  Making coffee. The melody gets a little more active, warmer.
                   We shift to F lydian (#4 gives a hopeful, slightly magical
                   quality — the smell of coffee filling the room).

  A' (bars 17-24): Looking out at Lake Washington through the rain. Back to
                    D dorian but the melody is higher, more awake. The rain
                    pattern is still there. It's peaceful now, not sleepy.

  Coda (bars 25-28): A single held chord dissolving. You put on your jacket
                      and step outside.

Tempo: 72 BPM — slow enough to feel the rain.
"""

from midiutil import MIDIFile
import os

midi = MIDIFile(3)  # rain, melody, bass
TEMPO = 72

for t in range(3):
    midi.addTempo(t, 0, TEMPO)

# Track 0: Rain drops — high register repeated notes, soft, slightly random velocity
# Track 1: Melody — right hand
# Track 2: Bass/chords — left hand

# ============================================================
# D Dorian: D E F G A B C D  (like C major starting on D)
# F Lydian: F G A B C D E F  (like C major starting on F, with #4 = B)
# ============================================================

import random
random.seed(2026)

# --- RAIN (Track 0, channel 0) ---
# Gentle repeated notes in the high register, like raindrops on glass
# Use notes from the scale, randomly picked, soft dynamics
rain_notes_dorian = [86, 84, 81, 79, 77]  # D6, C6, A5, G5, F5
rain_notes_lydian = [89, 88, 86, 84, 81]  # F6, E6, D6, C6, A5

def write_rain(start_beat, bars, note_pool, base_vel=35):
    """Eighth-note raindrops with random pitch from pool, varying velocity."""
    for i in range(bars * 8):  # 8 eighths per bar
        t = start_beat + i * 0.5
        pitch = random.choice(note_pool)
        vel = base_vel + random.randint(-8, 12)
        # Occasionally skip a drop (rest) for naturalness
        if random.random() < 0.15:
            continue
        midi.addNote(0, 0, pitch, t, 0.4, vel)

# Section A rain
write_rain(0, 8, rain_notes_dorian, 33)
# Section B rain (slightly less, coffee warmth takes over)
write_rain(32, 8, rain_notes_lydian, 28)
# Section A' rain
write_rain(64, 8, rain_notes_dorian, 30)
# Coda — rain fading
write_rain(96, 4, rain_notes_dorian, 22)

# --- BASS / LEFT HAND (Track 2, channel 2) ---
# Slow whole-note pads providing the harmonic foundation

# Section A: Dm - Am/C - Bb - C  (dorian, 2 bars each)
bass_a = [
    ([50, 53, 57], 8),  # Dm (D3 F3 A3)
    ([48, 52, 57], 8),  # Am/C (C3 E3 A3)
    ([46, 50, 53], 8),  # Bb (Bb2 D3 F3)
    ([48, 52, 55], 8),  # C (C3 E3 G3)
]

# Section B: Fmaj7 - G - Am - Fmaj7 (lydian warmth)
bass_b = [
    ([53, 57, 60, 64], 8),  # Fmaj7 (F3 A3 C4 E4)
    ([55, 59, 62], 8),      # G (G3 B3 D4)
    ([57, 60, 64], 8),      # Am (A3 C4 E4)
    ([53, 57, 60, 64], 8),  # Fmaj7
]

# Section A': same as A
# Coda: Dm9 held
bass_coda = [([50, 53, 57, 60, 64], 16)]  # Dm9 dissolving

def write_chords(start, chord_list, vel=50):
    t = start
    for notes, dur in chord_list:
        for n in notes:
            midi.addNote(2, 2, n, t, dur, vel)
        t += dur

write_chords(0, bass_a, 50)
write_chords(32, bass_b, 48)
write_chords(64, bass_a, 45)
write_chords(96, bass_coda, 38)

# --- MELODY (Track 1, channel 1) ---
# Section A: Slow, waking up. Long notes with rests. D dorian.
# The melody should feel like stretching — rising gently.

melody_a = [
    # bar 1-2: just a few notes, you're barely awake
    (62, 0, 3, 55),    # D4 — eyes open
    (64, 4, 2, 50),    # E4 — blink
    (65, 7, 3, 55),    # F4 — sigh
    # bar 3-4: a little more
    (67, 12, 2, 60),   # G4
    (69, 14.5, 1.5, 58), # A4
    (67, 16, 4, 55),   # G4 — settle back
    # bar 5-6: reaching up
    (69, 22, 2, 62),   # A4
    (72, 24, 3, 65),   # C5 — ah, awake now
    (71, 28, 2, 58),   # B4
    # bar 7-8: gentle descent
    (69, 30, 2, 60),   # A4
    (67, 32 - 2, 2, 55), # G4 — breathe
]

# Section B: More movement. Coffee energy. F lydian brightness.
melody_b = [
    # bar 9-10
    (65, 32, 1.5, 65),   # F4 — coffee's ready
    (67, 33.5, 1, 62),   # G4
    (69, 35, 1.5, 68),   # A4
    (71, 37, 2, 70),     # B4 — lydian #4! warmth
    (72, 39.5, 2, 68),   # C5
    # bar 11-12
    (74, 42, 1, 65),     # D5
    (72, 43, 1, 62),     # C5
    (71, 44.5, 1.5, 68), # B4 — that #4 again
    (69, 46, 2, 65),     # A4
    (72, 48 - 0.5, 2, 62), # C5
    # bar 13-14
    (74, 50, 2, 70),     # D5 — peak
    (76, 52, 1.5, 72),   # E5
    (74, 54, 1, 65),     # D5
    (72, 55.5, 2.5, 68), # C5
    # bar 15-16: settle into warmth
    (71, 58, 1.5, 65),   # B4
    (69, 60, 2, 62),     # A4
    (65, 62, 2, 58),     # F4 — home
]

# Section A': D dorian again, but higher register, more awake
melody_a2 = [
    # bar 17-18
    (74, 64, 2, 62),     # D5 — same melody, octave up feeling
    (76, 66.5, 1.5, 60),
    (77, 68, 3, 65),     # F5
    # bar 19-20
    (79, 72, 2, 68),     # G5
    (81, 74, 1.5, 65),   # A5
    (79, 76, 3, 60),     # G5
    # bar 21-22
    (81, 80, 2, 68),     # A5
    (84, 82, 2.5, 72),   # C6 — looking out at the lake
    (83, 85, 1.5, 62),   # B5
    # bar 23-24
    (81, 87, 2, 60),     # A5
    (79, 89, 2, 55),     # G5
    (74, 92, 3, 50),     # D5 — peaceful
]

# Coda: one last note, fading
melody_coda = [
    (62, 96, 6, 45),     # D4 — back where we started
    (65, 103, 8, 30),    # F4 — held, dissolving into rain
]

def write_melody(notes):
    for pitch, start, dur, vel in notes:
        midi.addNote(1, 1, pitch, start, dur, vel)

write_melody(melody_a)
write_melody(melody_b)
write_melody(melody_a2)
write_melody(melody_coda)

# Write
out = os.path.expanduser('~/clawspace/melody-experiment/kirkland-rain.mid')
with open(out, 'wb') as f:
    midi.writeFile(f)
print(f"🌧️ Wrote {out}")
