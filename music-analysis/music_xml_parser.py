from music21 import *
from collections import defaultdict 

# filename = "AP Music Theory 2022 Q5.mxl"
filename = "music-xml-examples/voice-leading-7.musicxml"
#filename = "../music-xml-examples/bad-voice-leading.musicxml"

'''
TODO
Remove Chord_Transition and attach melodic intervals to Chord_Wrapper
Store Chord_Wrappers in sorted list (short function or comparison function)
'''
class ChordWrapper:
    # set on init
    notes = None # list of 4 notes
    chord_obj = None # "chord" taken by music21 module

    # set externally
    prev_chord = None
    next_chord = None

    # calculated by analyze
    location = None # (measure number, offset)
    duration = None 
    inversion = None # 0, 1, 2
    harmonic_intervals = {} # dictionary of intervals (note_index_1, note_index_2)
    degrees = {} # dictionary of integers 1-8 (note_index)
    quality = None # major, minor, diminished, augmented, other
    incomplete = None # incomplete major or incomplete minor (dyad of root and maj/min third)
    isSeventh = None # true if all 4 notes in seventh chord are present
    rn = None # music21 roman numeral

    def __init__(self, v1, v2, v3, v4):
        self.notes = [v1, v2, v3, v4] # notes preserve duration; chord does not
        self.chord_obj = chord.Chord([no.pitch.name for no in self.notes])

    def analyze(self, key):
        # inversions
        self.inversion = self.chord_obj.inversion()

        # harmonic intervals
        for a in range(len(self.notes)-1):
            for b in range(a+1, len(self.notes)):
                self.harmonic_intervals[(a, b)] = interval.Interval(self.notes[a], self.notes[b])

        # scale degrees
        sc = key.getScale()
        for a in range(len(self.notes)):
            self.degrees[a] = sc.getScaleDegreeFromPitch(self.notes[a].pitch)

        # quality
        self.quality = self.chord_obj.quality

        # incomplete
        self.incomplete = self.chord_obj.isIncompleteMajorTriad() or self.chord_obj.isIncompleteMinorTriad()

        # isSeventh
        self.isSeventh = self.chord_obj.isSeventh()

        # location
        self.location = tuple((self.notes[0].measureNumber, self.notes[0].offset))

        # duration
        self.duration = self.notes[0].duration.quarterLength

        # roman numerals, chord quality
        self.rn = roman.romanNumeralFromChord(self.chord_obj, key)

    def __str__(self):
        message = f''
        # message += f'{self.name}\n'
        message += f'{self.notes}\n'
        # message += f'{self.intervals}\n'
        return message

class ScoreWrapper:
    key = None
    key_signature = None
    key_interpretations = []
    chord_transitions = []
    chord_wrappers = []
    score = None

    # store chords and location

    def __init__(self, score):
        self.score = score
        self.key = score.analyze("key")
        self.key_signature = score[2][1].keySignature
        self.key_interpretations = score.analyze("key").alternateInterpretations[0:3]
        self.parseScore()
        self.format_chord_wrappers()

    def __str__(self):
        return f"score({self.key})"
    
    def parseScore(self):
        voice_map = {}
        note_matrix = {}
        locations = set()
        for voice in self.score.recurse().voices: # 2 staffs per score; n measures per staff, 2 voices per measure
            # map voice to number
            vox = str(voice)[-2]
            if vox not in voice_map:
                voice_map[vox] = len(voice_map)

            for no in voice.notes:
                measure_num = no.measureNumber
                offset = no.offset
                locations.add((measure_num, offset))
                note_matrix[(measure_num, offset, voice_map[vox])] = no

        chords = []
        for location in locations:
            chords.append(ChordWrapper(note_matrix[(location[0], location[1], 0)], 
                                    note_matrix[(location[0], location[1], 1)], 
                                    note_matrix[(location[0], location[1], 2)], 
                                    note_matrix[(location[0], location[1], 3)]))
        self.chord_wrappers = chords

    def format_chord_wrappers(self):
        #TODO: sort chords by location here
            
        #TODO: set previous and next chord links within chord wrappers here

        # set all chord wrapper attributes here
        for i in range(len(self.chord_wrappers)):
            self.chord_wrappers[i].analyze(self.key)

class ChordTransition:
    chord_prev = None # ChordWrapper
    chord_next = None # ChordWrapper
    intervals = {} # dictionary of intervals (note_index)

    def __init__(self, chord_prev, chord_next):
        self.chord_prev = chord_prev
        self.chord_next = chord_next

    def analyze(self):
        # melodic intervals
        for a in range(len(self.chord_prev.notes)):
            self.intervals[a] = interval.Interval(self.chord_prev.notes[a], self.chord_next.notes[a])

    def __str__(self):
        return f"[{self.chord_prev}, {self.chord_next}]"

if __name__ == '__main__':
    s = converter.parse(filename)
    sw = ScoreWrapper(s)
    print(sw)

    for c in sw.chord_wrappers:
        print(c)


