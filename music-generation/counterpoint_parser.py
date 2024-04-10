import copy

from music21 import *
import os

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
            #print("0: ", self.interval_wrappers[0] if len(self.interval_wrappers) > 0 else None)
            iw = IntervalWrapper(n, self.cf)
            print(iw)
            self.interval_wrappers.append(iw)
            for i in range(0, len(self.interval_wrappers)):
                print(i, ": ", self.interval_wrappers[i])

        print()
        for el in self.interval_wrappers:
            print(el)

class IntervalWrapper:
    cf = None # cantus firmus index (0 or 1)
    cp = None # counterpoint index (0 or 1)

    notes = [None, None]
    interval_obj = None # interval
    intervalClass = None

    prev = None
    next = None

    #quality = None

    def __init__(self, n, cantus_firmus):
        self.cf = cantus_firmus
        self.cp = int(not cantus_firmus)
        self.notes[self.cf] = note.Note(n.pitch)

    def __str__(self):
        return f"{self.notes[0].pitch if self.notes[0] is not None else None}, {self.notes[1].pitch if self.notes[1] is not None else None}: {self.interval_obj.name if self.interval_obj is not None else None}"

    def harmonize(self, note):
        print(self)
        print(self.cp)
        self.notes[self.cp] = note
        self.interval_obj = interval.Interval(self.notes[0], self.notes[1])
        self.intervalClass = self.interval_obj.intervalClass

if __name__ == '__main__':
    cantus_firmus = 1

    s = converter.parse(fn1)

    sw = ScoreWrapper(s, cantus_firmus)

    s2 = converter.parse(fn2)
    harmony = []
    for n in s2.recurse().getElementsByClass(note.Note):
        harmony.append(n)

    print()

    for i in range(0, len(sw.interval_wrappers)):
        #print(sw.interval_wrappers[i])
        sw.interval_wrappers[i].harmonize(harmony[i])
        #print(sw.interval_wrappers[i])

    # for el in s.recurse():
    #     print(el)
    #
    # print("=========")
    #
    # for a in s.getElementsByClass(stream.Part):
    #     for b in a.recurse().getElementsByClass(note.Note):
    #         print(b)
    #
    # print("----------")
    #
    # for el in s.recurse().getElementsByClass(note.Note):
    #     print(el)