"""
实验3: Blues Night — A Blues Scale 即兴 — Claw 🦞
=================================================
在试什么：用 A blues scale (A C D Eb E G) 写一段有 swing feel
的12小节 blues。三轨配器：电钢琴旋律 + 低音提琴 walking bass + 轻打击乐。

为什么：Blues 是情感最直接的音乐形式。Swing feel 通过不等分的
八分音符（长-短）创造摇摆感。Walking bass 每拍一个音，像心跳。

场景：Kirkland 深夜，I-405 北向，车窗半开，湖面的灯光在右边闪。
不急着到哪里去。

发现：Swing 的关键是 triplet feel — 第一个八分音符占 2/3 拍，
第二个占 1/3。Walking bass 在和弦音之间加经过音，让低音线流动。
Eb (blue note) 是灵魂所在——半音的紧张感。
"""

from midiutil import MIDIFile
import random

random.seed(405)  # I-405 🛣️

midi = MIDIFile(3)
tempo = 78  # slow, late night

for i, name in enumerate(["Rhodes Piano", "Upright Bass", "Brushes"]):
    midi.addTrackName(i, 0, name)
    midi.addTempo(i, 0, tempo)

# GM: 4=Rhodes, 32=Acoustic Bass, ch9=drums
midi.addProgramChange(0, 0, 0, 4)   # Electric Piano 1
midi.addProgramChange(1, 1, 0, 32)  # Acoustic Bass

# A blues scale: A2=45, A3=57, A4=69
blues_scale = [69, 72, 74, 75, 76, 79, 81]  # A4 C5 D5 Eb5 E5 G5 A5

# Swing helper: pairs of eighths become (2/3 + 1/3) of a beat
def swing_pair(start, pitch1, pitch2, track=0, ch=0, vel=75):
    long = 2/3
    short = 1/3
    if pitch1:
        midi.addNote(track, ch, pitch1, start, long * 0.9, vel)
    if pitch2:
        midi.addNote(track, ch, pitch2, start + long, short * 0.9, vel - 5)

# 12-bar blues in A: A7(4) | D7(2) | A7(2) | E7(1) | D7(1) | A7(2)
chord_roots_12bar = [
    57, 57, 57, 57,   # bars 1-4: A
    62, 62,            # bars 5-6: D
    57, 57,            # bars 7-8: A
    64,                # bar 9: E
    62,                # bar 10: D
    57, 57,            # bars 11-12: A
]

# === MELODY (Rhodes) ===
# Pre-composed phrases with blues feel
melody_phrases = [
    # bar 1-2: opening statement
    [(0, 69, 1.5), (1.5, 72, 0.5), (2, 74, 1), (3, 75, 0.5), (3.5, 76, 0.5),
     (4, 79, 2), (6, 76, 1), (7, 0, 1)],
    # bar 3-4: response
    [(0, 75, 0.67), (0.67, 76, 0.33), (1, 79, 1.5), (2.5, 76, 0.5), (3, 74, 1),
     (4, 72, 1.5), (5.5, 69, 0.5), (6, 72, 2)],
    # bar 5-6: D chord area - reach higher
    [(0, 74, 0.67), (0.67, 75, 0.33), (1, 79, 1), (2, 81, 1.5), (3.5, 79, 0.5),
     (4, 76, 1), (5, 75, 0.67), (5.67, 74, 0.33), (6, 72, 2)],
    # bar 7-8: back to A, settling
    [(0, 69, 1), (1, 72, 0.67), (1.67, 74, 0.33), (2, 76, 2),
     (4, 75, 0.67), (4.67, 74, 0.33), (5, 72, 1), (6, 69, 2)],
    # bar 9-10: turnaround tension
    [(0, 76, 1), (1, 79, 1), (2, 81, 1.5), (3.5, 79, 0.5),
     (4, 76, 0.67), (4.67, 75, 0.33), (5, 74, 1), (6, 72, 1), (7, 69, 1)],
    # bar 11-12: resolution
    [(0, 72, 1), (1, 74, 0.67), (1.67, 72, 0.33), (2, 69, 3),
     (5, 0, 1), (6, 69, 2)],
]

bar = 0
phrase_bars = [2, 2, 2, 2, 2, 2]
for i, phrase in enumerate(melody_phrases):
    beat_offset = bar * 4
    for note_t, pitch, dur in phrase:
        if pitch > 0:
            vel = random.randint(65, 85)
            midi.addNote(0, 0, pitch, beat_offset + note_t, dur * 0.9, vel)
    bar += phrase_bars[i]

# === WALKING BASS ===
# Walking bass: chord tone on beat 1, chromatic/scale approach to next
bass_notes_per_bar = {
    57: [45, 47, 48, 50],   # A: A E F G (approach to next)
    62: [50, 52, 53, 52],   # D: D F# G F# 
    64: [52, 51, 50, 47],   # E: E Eb D B (descending approach)
}

for bar_idx, root in enumerate(chord_roots_12bar):
    beat_offset = bar_idx * 4
    notes = bass_notes_per_bar[root]
    # Vary the last note to approach next bar's root
    if bar_idx < 11:
        next_root = chord_roots_12bar[bar_idx + 1]
        next_bass = bass_notes_per_bar[next_root][0]
        # chromatic approach from below or above
        if random.random() > 0.5:
            notes = list(notes)
            notes[3] = next_bass - 1  # half step below
    for beat, pitch in enumerate(notes):
        vel = 70 + (5 if beat == 0 else 0)  # accent beat 1
        midi.addNote(1, 1, pitch, beat_offset + beat, 0.9, vel)

# === BRUSHES (channel 9) ===
# Light brush pattern: ride cymbal + cross-stick + hi-hat
for bar_idx in range(12):
    beat_offset = bar_idx * 4
    for beat in range(4):
        t = beat_offset + beat
        # Ride cymbal (51) on every beat, lighter on 2&4
        vel = 50 if beat % 2 == 0 else 40
        midi.addNote(2, 9, 51, t, 0.9, vel)
        # Cross stick (37) on beats 2 and 4
        if beat in (1, 3):
            midi.addNote(2, 9, 37, t, 0.5, 45)
        # Swing eighths on ride - ghost note
        midi.addNote(2, 9, 51, t + 2/3, 0.3, 30)

# Final sustained A
midi.addNote(0, 0, 69, 48, 4, 60)
midi.addNote(1, 1, 45, 48, 4, 65)

with open("blues_night.mid", "wb") as f:
    midi.writeFile(f)

print("✅ blues_night.mid generated")
