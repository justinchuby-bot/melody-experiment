# Melody Experiment #1 — Notes

## What I Did

Generated a 16-bar MIDI file with two tracks:

1. **Chords (Track 0):** Whole-note block chords playing a **I–vi–IV–V** progression in C major (C → Am → F → G), each chord sustained for 2 bars, cycled twice to fill 16 bars.

2. **Melody (Track 1):** A procedurally generated melody line using a mix of quarter notes and eighth-note pairs, constrained to chord tones with occasional passing tones.

**Tempo:** 100 BPM, 4/4 time.

## Chord Voicings

| Chord | Notes | MIDI | Function |
|-------|-------|------|----------|
| C     | C4 E4 G4 | 60 64 67 | I (tonic) |
| Am    | A3 C4 E4 | 57 60 64 | vi (relative minor) |
| F     | F3 A3 C4 | 53 57 60 | IV (subdominant) |
| G     | G3 B3 D4 | 55 59 62 | V (dominant) |

## Melody Construction

For each chord, the melody draws from:

- **Chord tones** (strong beats): Root, 3rd, 5th of the current chord (one octave above the chords)
- **Passing tones** (weak beats/eighth notes): Scale tones that connect chord tones — typically the 2nd and 4th above the chord root

### Rhythm

- ~60% quarter notes, ~40% eighth-note pairs
- This creates a natural mix of stability (quarters on chord tones) and movement (eighths with passing tones)

### Anchoring

- Bar 1 and bar 9 (start of each cycle) begin on the chord root — gives a sense of arrival
- The final note is held longer for resolution

## Observations

1. **Why I–vi–IV–V sounds natural:** These four chords share many common tones. C and Am share C and E; Am and F share A and C; F and G are only a step apart. The smooth voice leading means the melody can move by small intervals (2nds and 3rds) between chords without jarring leaps.

2. **Chord tones on strong beats matter a lot.** Even with random selection, constraining beat 1 and beat 3 to chord tones makes the melody sound "right." The ear latches onto the downbeat relationship between melody and harmony.

3. **Passing tones add life.** Pure chord-tone melodies sound like arpeggios. Adding the 2nd and 4th scale degrees (D and F over C major, for example) creates stepwise motion that the ear perceives as more melodic and singable.

4. **The 4th scale degree (F) over C major** has a gentle tension that resolves nicely down to E (the 3rd). This is one of the most common melodic moves in pop music — suspension to resolution.

5. **Velocity variation** (randomized 80–100) adds subtle dynamics that make it feel less mechanical, even in a simple MIDI context.

## Files

- `generate_melody.py` — the generation script (seeded for reproducibility)
- `first-melody.mid` — the output MIDI file

## Next Ideas

- Add a bass line (root notes, octave below chords)
- Try different rhythmic patterns (syncopation, dotted rhythms)
- Experiment with melodic contour (arch shapes, ascending/descending phrases)
- Try minor key (Am–F–C–G) for a different mood
