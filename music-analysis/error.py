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
    title = None
    location = None
    description = None
    voices = [False] * 4
    suggestion = None
    duration = None
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

    # rule 27: key signatures
    if (sw.key != sw.key_signature):
        title = "Key Signature Error"
        location = 0 # set the location correctly later
        description = "Your voice leading is most suitable for another key signature."
        suggestion = f"Suggested key: {sw.key}"

        accidentals = sw.key.sharps
        if accidentals > 1: # surprised there is nothing in music21 for this
            suggestion += f" ({accidentals} shaprs)"
        elif accidentals == 0:
            suggestion += f" (no accidentals)"
        else:
            suggestion += f" ({abs(accidentals)} flats)"

        errors.append(Error(title, location, description, suggestion))

    # rule 1: ranges

    # rule 2: spacing

    # rule 3: crossing

    # rule 4: overlapping

    # rule 5: leaping once

    # rule 6: leaping twice

    # rule 7: large leaps

    # rule 8: leaps of diminished quality

    # rule 9: resolution of 7^

    # rule 10: chords

    # rule 11: parallel octaves

    # rule 12: parallel 5ths

    # rule 13: hidden 5ths and octaves


    return errors

if __name__ == '__main__':
    sw = music_xml_parser.getScoreWrapper(filename)
    print(sw)

    errors = getErrors(sw)

    for e in errors:
        print(e)

