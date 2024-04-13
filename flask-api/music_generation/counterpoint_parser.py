import copy
from music21 import *

ranges = [["D2", "D4"], ["C4", "A5"]]
notes_in_range = [["D2", "D#2", "E-2", "E2", "F2", "F#2", "G-2", "G2", "G#2", "A-2", "A2", "A#2", "B-2", "B2",
                   "C3", "C#3", "D-3", "D3", "D#3", "E-3", "E3", "F3", "F#3", "G-3", "G3", "G#3", "A-3", "A3", "A#3", "B-3", "B3",
                   "C4", "C#4", "D-4"],
                  ["C4", "C#4", "D-4", "D4", "D#4", "E-4", "E4", "F4", "F#4", "G-4", "G4", "G#4", "A-4", "A4", "A#4", "B-4", "B4",
                   "C5", "C#5", "D-5", "D5", "D#5", "E-5", "E5", "F5", "F#5", "G-5", "G5", "G#5", "A-5", "A5"]]
consonant_intervals = ["P1", "m3", "M3", "P5", "m6", "M6",
                       "P8", "m10", "M10", "P12", "m13", "M13",
                       "P15", "m17", "M17", "P19", "m20", "M20",
                       "P22", "m24", "M24", "P26"]

fn1 = "./melody2.musicxml"
fn2 = "./harmony2.musicxml"

class ScoreWrapper:
    score = None
    cf = None  # cantus firmus index (0 or 1)
    cp = None  # counterpoint index (0 or 1)
    interval_wrappers = []

    def __init__(self, score, cantus_firmus):
        self.score = score
        self.cf = cantus_firmus
        self.cp = int(not cantus_firmus)

        for n in score.recurse().getElementsByClass(note.Note):
            iw = IntervalWrapper(n, self.cf)
            self.interval_wrappers.append(iw)

        for i in range(len(self.interval_wrappers)):
            if i != 0:
                self.interval_wrappers[i].prev = self.interval_wrappers[i-1]
            if i != len(self.interval_wrappers)-1:
                self.interval_wrappers[i].next = self.interval_wrappers[i+1]

    def calc_vlqs(self):
        for iw in self.interval_wrappers:
            if iw.next is not None:
                iw.melodic_intervals = [interval.Interval(iw.notes[0], iw.next.notes[0]), interval.Interval(iw.notes[1], iw.next.notes[1])]
                iw.vlq = voiceLeading.VoiceLeadingQuartet(iw.notes[0], iw.next.notes[0], iw.notes[1], iw.next.notes[1])
                iw.vlq.key = key.Key(self.interval_wrappers[len(self.interval_wrappers)-1].notes[0].name.lower())

class IntervalWrapper:
    cf = None # cantus firmus index (0 or 1)
    cp = None # counterpoint index (0 or 1)

    def __init__(self, n, cantus_firmus):
        self.cf = cantus_firmus
        self.cp = int(not cantus_firmus)
        self.notes = [None, None]
        self.notes[self.cf] = n
        self.interval_obj = None  # interval
        self.intervalClass = None
        self.prev = None
        self.next = None
        self.counterpoints = []
        self.melodic_intervals = None
        self.vlq = None

        # possible harmonies
        for n2 in notes_in_range[self.cp]:
            mel = (n if cantus_firmus == 0 else note.Note(n2))
            har = (n if cantus_firmus == 1 else note.Note(n2))
            i = interval.Interval(har, mel)
            if i.name in consonant_intervals:
                self.counterpoints.append(n2)

    def __str__(self):
        return f"{self.notes[0].pitch if self.notes[0] is not None else None}, {self.notes[1].pitch if self.notes[1] is not None else None}: {self.interval_obj.name if self.interval_obj is not None else None}"

    def harmonize(self, note):
        self.notes[self.cp] = note
        self.interval_obj = interval.Interval(self.notes[0], self.notes[1])
        self.intervalClass = self.interval_obj.intervalClass

def getScoreWrapper(fn, cantus_firmus):
    s = converter.parse(fn)
    sw = ScoreWrapper(s, cantus_firmus)
    return sw

def testHarmony(sw, fn2):
    s2 = converter.parse(fn2)
    harmony = []
    for n in s2.recurse().getElementsByClass(note.Note):
        harmony.append(n)
    for i in range(0, len(sw.interval_wrappers)):
        sw.interval_wrappers[i].harmonize(harmony[i])
    sw.calc_vlqs()

if __name__ == '__main__':
    cantus_firmus = 1

    s = converter.parse(fn1)
    sw = ScoreWrapper(s, cantus_firmus)

    testHarmony(sw, fn2)


