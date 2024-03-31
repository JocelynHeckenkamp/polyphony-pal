from music21 import *
from . import music_xml_parser as mxp
from . import music21_method_extensions

music21_method_extensions.extend()


# TODO: Try different approach: maybe try to assign the octaves to the chord tones based on the voice range?
def getVoiceRanges():
    ranges = [
        ('C4', 'C#4', 
        'D-4', 'D4', 'D#4', 
        'E-4', 'E4', 'E#4', 
        'F-4', 'F4', 'F#4', 
        'G-4', 'G4', 'G#4', 
        'A-4', 'A4', 'A#4', 
        'B-4', 'B4', 'B#4',
        'C-5', 'C5', 'C#5',
        'D-5', 'D5', 'D#5', 
        'E-5', 'E5', 'E#5', 
        'F-5', 'F5', 'F#5', 
        'G-5', 'G5'),  # soprano

        ('G3', 'G#3', 
        'A-3', 'A3', 'A#3', 
        'B-3', 'B3', 'B#3',
        'C-4', 'C4', 'C#4', 
        'D-4', 'D4', 'D#4', 
        'E-4', 'E4', 'E#4', 
        'F-4', 'F4', 'F#4', 
        'G-4', 'G4', 'G#4', 
        'A-4', 'A4', 'A#4', 
        'B-4', 'B4', 'B#4',
        'C-5', 'C5'),  # alto

        ('C3', 'C#3', 
        'D-3', 'D3', 'D#3', 
        'E-3', 'E3', 'E#3', 
        'F-3', 'F3', 'F#3', 
        'G-3', 'G3', 'G#3', 
        'A-3', 'A3', 'A#3', 
        'B-3', 'B3', 'B#3',
        'C-4', 'C4', 'C#4', 
        'D-4', 'D4', 'D#4', 
        'E-4', 'E4', 'E#4', 
        'F-4', 'F4', 'F#4', 
        'G-4', 'G4'),  # tenor

        ('E2', 'E#2', 
        'F-2', 'F2', 'F#2', 
        'G-2', 'G2', 'G#2', 
        'A-2', 'A2', 'A#2', 
        'B-2', 'B2', 'B#2',
        'C-3', 'C3', 'C#3',
        'D-3', 'D3', 'D#3', 
        'E-3', 'E3', 'E#3', 
        'F-3', 'F3', 'F#3', 
        'G-3', 'G3', 'G#3', 
        'A-3', 'A3', 'A#3', 
        'B-3', 'B3', 'B#3',
        'C-4', 'C4')  # bass
    ]

    # make notes out of the pitch names
    noteRanges = []
    for voice in ranges:
        noteRanges.append(tuple(map(lambda x: note.Note(x), voice)))
    return noteRanges


def analyzeRN(rnStr, keyStr):
    # write bassline
    bassline = []
    chordPitches = []
    for rn in rnStr:
        c = roman.RomanNumeral(rn, key.Key(keyStr)).pitches
        ch = chord.Chord(c)
        chordPitches.append( list(map((lambda x : x.name), ch.notes)) )
        bassline.append(ch.root())
    return bassline, chordPitches
