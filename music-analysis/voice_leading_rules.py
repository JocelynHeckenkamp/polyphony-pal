from music21 import *
import music_xml_parser

filename = "../music-xml-examples/voice-leading-7.musicxml"

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
    title = None
    location = None
    description = None
    suggestion = None
    def __init__(self, title, location, description, suggestion):
        self.title = title
        self.location = location
        self.description = description
        self.suggestion = suggestion

    def __str__(self):
        return f"{self.title({self.location})}"

def getErrors(sw):
    errors = []

    # key signature
    if (sw.key != sw.key_signature):
        title = "Key Signature Error"


    return errors

if __name__ == '__main__':
    sw = music_xml_parser.getScoreWrapper(filename)
    print(sw)

    errors = getErrors()
    print(errors)


