from music21 import *
from collections import defaultdict 

# filename = "AP Music Theory 2022 Q5.mxl"
filename = "../music-xml-examples/voice-leading-7.musicxml"
#filename = "../music-xml-examples/bad-voice-leading.musicxml"

class ScoreWrapper:
    key = None
    key_signature = None
    key_interpretations = []
    chord_transitions = []
    def __init__(self, score):
        self.key = score.analyze("key")
        self.key_signature = score[2][1].keySignature
        self.key_interpretations = score.analyze("key").alternateInterpretations[0:3]

    def __str__(self):
        return f"score({self.key})"

class ChordWrapper:
    notes = None
    chord_obj = None # "chord" taken by music21 module
    inversion = None
    intervals = {}
    degrees = {}
    name = None
    rn = None

    def __init__(self, v1, v2, v3, v4):
        self.notes = [v1, v2, v3, v4] # notes preserve duration; chord does not
        self.chord_obj = chord.Chord([no.pitch.name for no in self.notes])

    def analyze(self, key):
        # inversions
        self.inversion = self.chord_obj.inversion()

        # harmonic intervals
        for a in range(len(self.notes)-1):
            for b in range(a+1, len(self.notes)):
                self.intervals[(a, b)] = interval.Interval(self.notes[a], self.notes[b])

        # scale degrees
        sc = key.getScale()
        #for no in self.notes:
        for a in range(len(self.notes)):
            self.degrees[a] = sc.getScaleDegreeFromPitch(self.notes[a].pitch)

        # roman numerals, chord quality
        self.rn = roman.romanNumeralFromChord(self.chord_obj, key)

    def __str__(self):
        message = f''
        # message += f'{self.name}\n'
        message += f'{self.notes}\n'
        # message += f'{self.intervals}\n'
        return message

class ChordTransition:
    chord_prev = None
    chord_next = None
    intervals = {}

    def __init__(self, chord_prev, chord_next):
        self.chord_prev = chord_prev
        self.chord_next = chord_next

    def analyze(self):
        # melodic intervals
        for a in range(len(self.chord_prev.notes)):
            self.intervals[a] = interval.Interval(self.chord_prev.notes[a], self.chord_next.notes[a])

    def __str__(self):
        return f"[{self.chord_prev}, {self.chord_next}]"

def parse_XML(filename):
    s = converter.parse(filename)
    sw = ScoreWrapper(s)

    voice_map = {}
    note_matrix = {}
    locations = set()
    for voice in s.recurse().voices: # 2 staffs per score; n measures per staff, 2 voices per measure
        # map voice to number
        vox = str(voice)[-2]
        if vox not in voice_map:
            voice_map[vox] = len(voice_map)

        for no in voice.notes:
            measure_num = no.measureNumber
            offset = no.offset
            locations.add((measure_num, offset))
            note_matrix[(measure_num, offset, voice_map[vox])] = no

    chords = {}
    chord_transitions = []
    chord_prev = None
    for id, location in enumerate(locations):
        chords[location] = ChordWrapper(note_matrix[(location[0], location[1], 0)], note_matrix[(location[0], location[1], 1)], note_matrix[(location[0], location[1], 2)], note_matrix[(location[0], location[1], 3)])
        chords[location].analyze(sw.key)
        if (id > 0):
            chord_transitions.append(ChordTransition(chord_prev, chords[location]))
            chord_transitions[-1].analyze()
        chord_prev = chords[location]

    sw.chord_transitions = chord_transitions
    return chords, locations, sw

if __name__ == '__main__':
    chords, locations, sc = parse_XML(filename)

    for location in locations:
        print(chords[location])


