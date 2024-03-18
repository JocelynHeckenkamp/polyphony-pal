from music21 import *
from collections import defaultdict 
from functools import cmp_to_key

# filename = "AP Music Theory 2022 Q5.mxl"
fn = "./music-xml-examples/UnitTest14.musicxml"
#filename = "../music-xml-examples/bad-voice-leading.musicxml"

class ChordWrapper:
    # set on init
    notes = None # list of 4 notes
    chord_obj = None # "chord" taken by music21 module

    # set externally
    prev = None
    next = None

    # calculated by analyze
    location = None                     # (measure number, offset)
    duration = None                     # quarterlength of first note in chord (assume all notes in chord are same length)
    inversion = None                    # 0, 1, 2
    harmonic_intervals = {}             # dictionary of harmonic intervals (note_index_1, note_index_2)
    melodic_intervals = {}              # dictionary of melodic intervals (note_index)
    degrees = {}                        # dictionary of integers 1-8 (note_index)
    quality = None                      # major, minor, diminished, augmented, other
    incomplete = None                   # incomplete major or incomplete minor (dyad of root and maj/min third)
    isSeventh = None                    # true if all 4 notes in seventh chord are present
    rn = None                           # music21 roman numeral

    def __init__(self, v1, v2, v3, v4):
        self.notes = [v1, v2, v3, v4]   # notes preserve duration; chord does not
        self.chord_obj = chord.Chord([no for no in self.notes])
        self.melodic_intervals = {}
        self.harmonic_intervals = {}
        self.degrees = {}

    def set_location(self):
        # location
        self.location = tuple((self.notes[0].measureNumber, self.notes[0].offset))

    def analyze(self, key):
        # inversions
        self.inversion = self.chord_obj.inversion()

        # harmonic intervals
        for a in range(len(self.notes)-1):
            for b in range(a+1, len(self.notes)):
                self.harmonic_intervals[(a, b)] = interval.Interval(self.notes[a], self.notes[b])

        # melodic intervals
        for a in range(len(self.chord_obj.notes)):
            if self.next is not None:
                self.melodic_intervals[a] = interval.Interval(self.notes[a], self.next.notes[a])

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

        # duration
        self.duration = self.notes[0].duration.quarterLength

        # roman numerals, chord quality
        self.rn = roman.romanNumeralFromChord(self.chord_obj, key).romanNumeral

    def __str__(self):
        message = f'\n'
        message += f'{self.chord_obj.root()} {self.quality}'
        message += f' {self.rn}{(7 if self.isSeventh else "")}\n'
        message += f'{self.chord_obj.fullName}'
        return message

class ScoreWrapper:
    key = None
    key_signature = None
    key_interpretations = []
    chord_transitions = []
    chord_wrappers = []
    score = None

    def __init__(self, score):
        self.score = score
        self.key = score.analyze("key")
        self.key_signature = score.recurse().stream().keySignature
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
            chords[-1].set_location()
        self.chord_wrappers = chords

    def format_chord_wrappers(self):
        # sort chordwrappers by measure number first then offset number second
        def compare_chordWrapper(chord1, chord2):
            if chord1.location[0] == chord2.location[0]:
                return chord1.location[1] - chord2.location[1]
            else:
                return chord1.location[0] - chord2.location[0]
        self.chord_wrappers.sort(key=cmp_to_key(compare_chordWrapper))

        # link prev and next chord attributes
        for i in range(len(self.chord_wrappers)):
            if i != 0:
                self.chord_wrappers[i].prev = self.chord_wrappers[i-1]
            
            if i != len(self.chord_wrappers)-1:
                self.chord_wrappers[i].next = self.chord_wrappers[i+1]


        # set all chord wrapper attributes here
        for i in range(len(self.chord_wrappers)):
            self.chord_wrappers[i].analyze(self.key)

def getScoreWrapper(filename):
    s = converter.parse(filename)
    sw = ScoreWrapper(s)
    return sw

if __name__ == '__main__':
    sw = getScoreWrapper(fn)
    print(sw)

    #for c in sw.chord_wrappers:
        #print(c.location, c.chord_obj.fullName)
        #print(c.melodic_intervals)

    # chords iterated through by next pointer
    curr = sw.chord_wrappers[0]
    while(curr is not None):
        print(curr)
        curr = curr.next
    # s.show()


