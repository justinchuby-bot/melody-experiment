#!/usr/bin/env python3
"""Generate a 16-bar melody over a I-vi-IV-V progression in C major."""

from midiutil import MIDIFile
import random

random.seed(42)

midi = MIDIFile(2)  # 2 tracks: chords + melody
TEMPO = 100

# Track 0: chords, Track 1: melody
for t in range(2):
    midi.addTempo(t, 0, TEMPO)

# --- Chord progression: I-vi-IV-V, each chord = 2 bars, cycle twice = 16 bars ---
# MIDI note numbers (C4=60)
chords = {
    'C':  [60, 64, 67],      # C E G
    'Am': [57, 60, 64],      # A C E
    'F':  [53, 57, 60],      # F A C  (voiced low for warmth)
    'G':  [55, 59, 62],      # G B D
}
progression = ['C', 'Am', 'F', 'G']

# Write chords (track 0, channel 0) — each chord lasts 2 bars (8 beats)
beat = 0
for cycle in range(2):
    for name in progression:
        for note in chords[name]:
            midi.addNote(0, 0, note, beat, 8, 70)
        beat += 8

# --- Melody (track 1, channel 1) ---
# For each chord, define chord tones + available passing tones (all in octave 5, MIDI 72-84)
chord_info = {
    'C':  {'tones': [72, 76, 79],     'passing': [74, 77]},       # C5 E5 G5 | D5 F5
    'Am': {'tones': [69, 72, 76],     'passing': [71, 74]},       # A4 C5 E5 | B4 D5
    'F':  {'tones': [65, 69, 72],     'passing': [67, 71]},       # F4 A4 C5 | G4 B4
    'G':  {'tones': [67, 71, 74],     'passing': [69, 72]},       # G4 B4 D5 | A4 C5
}

def generate_melody_bar(chord_name, bar_start, bar_num):
    """Generate melody for one bar. Mix of quarter and eighth notes."""
    info = chord_info[chord_name]
    tones = info['tones']
    passing = info['passing']
    notes = []
    t = bar_start

    while t < bar_start + 4:
        remaining = bar_start + 4 - t
        # Decide rhythm: quarter (1 beat) or pair of eighths (1 beat total)
        if remaining >= 1 and random.random() < 0.6:
            # Quarter note — prefer chord tone
            pitch = random.choice(tones)
            notes.append((pitch, t, 1))
            t += 1
        elif remaining >= 0.5:
            # Two eighth notes: chord tone then passing tone (or vice versa)
            p1 = random.choice(tones)
            p2 = random.choice(passing) if random.random() < 0.5 else random.choice(tones)
            notes.append((p1, t, 0.5))
            notes.append((p2, t + 0.5, 0.5))
            t += 1
        else:
            break

    # Musical touches: first beat of bar 0 and bar 8 land on root
    if bar_num in (0, 8) and notes:
        notes[0] = (tones[0], notes[0][1], notes[0][2])
    # Last bar resolves to root
    if bar_num == 15 and notes:
        notes[-1] = (tones[0], notes[-1][1], 2)  # held note

    return notes

beat = 0
for cycle in range(2):
    for ci, name in enumerate(progression):
        for local_bar in range(2):
            bar_num = cycle * 8 + ci * 2 + local_bar
            melody_notes = generate_melody_bar(name, beat, bar_num)
            for pitch, start, dur in melody_notes:
                vel = random.randint(80, 100)
                midi.addNote(1, 1, pitch, start, dur, vel)
            beat += 4

# Write file
out_path = __import__('os').path.expanduser('~/clawspace/melody-experiment/first-melody.mid')
with open(out_path, 'wb') as f:
    midi.writeFile(f)

print(f"Wrote {out_path}")
