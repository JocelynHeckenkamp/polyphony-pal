from music21 import *
import music_xml_parser

#filename = "../music-xml-examples/voice-leading-7.musicxml"
filename = "../music-xml-examples/key-signature-error.musicxml"

'''
Error location types
- Two/three voices in one chord (e.g. spacing, crossing, doubling; rules 2, 3, 14-23)
- One voice (e.g. range; rule 1)
- One voice one transition (e.g.leaps > P8, resolutions; rules 5, 9, 24, 26)
- Two voices one transition (e.g. overlapping, parallel 5ths/octaves; rules 4, 11, 12, 13)
- One voice two transitions (e.g. two leaps not a triad; rules 6, 7, 8)
- Full chord (I64 chords; rules 10, 26)
- Full score (e.g. key signatures; rule 27)

Error locating
Option 1: error_start and error_end location tuples and list of voices -->  easier format for backend, could make highlighting easier in frontend
Option 2: error_start location tuple, number of chords it includes, and list of voices --> could make highlighting easier depending on how music is displayed
Option 3: list of notes it includes using location tuple (measure, offset, voice) --> most clearly shows how many notes are problematic and which ones; would make note color-coding easier

Could separate error types as melodic or harmonic corresponding with highlight vs circle in frontend
- Melodic (circled) errors: range, spacing crossing overalapping, leaps
- Harmonic (highlighted) errors: I64 chords, non-chords, resolution, doubling, incomplete chords
- Gray area (could be either one): parallel 5ths/octaves
- Other: key signature
'''

class Error:
    title = None # always has a value
    location = None # tuple of (measure, offset); measure is int 1-indexed; offset is float from 0.0-3.0
    description = None # description of the error; always has a value
    voices = [False] * 4 # array of 4 booleans; soprano, alto, tenor, bass; true means there's an error
    suggestion = None # does not always have a value
    duration = None # float; number of beats, usually 1.0, 2.0, or 3.0; -1 only for key signature error
    def __init__(self, title: str, location: tuple, description: str, suggestion: str, voices: list, duration: float):
        self.title = title
        self.location = location
        self.description = description
        self.suggestion = suggestion
        self.voices = voices
        self.duration = duration

    def __str__(self):
        #return f"{self.title} ({self.location})"
        return f"{self.title} ({self.location})\n - {self.description}\n - {self.suggestion}"

def getErrors(sw):
    errors = []

    return errors

if __name__ == '__main__':
    sw = music_xml_parser.getScoreWrapper(filename)
    print(sw)

    errors = getErrors(sw)

    for e in errors:
        print(e)

