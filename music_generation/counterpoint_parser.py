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
            iw = IntervalWrapper(n, self.cf)
            self.interval_wrappers.append(iw)

class IntervalWrapper:
    cf = None # cantus firmus index (0 or 1)
    cp = None # counterpoint index (0 or 1)

    #quality = None

    def __init__(self, n, cantus_firmus):
        self.cf = cantus_firmus
        self.cp = int(not cantus_firmus)
        self.notes = [None, None]
        self.notes[self.cf] = n
        self.interval_obj = None  # interval
        self.intervalClass = None
        self.prev = None
        self.next = None

    def __str__(self):
        return f"{self.notes[0].pitch if self.notes[0] is not None else None}, {self.notes[1].pitch if self.notes[1] is not None else None}: {self.interval_obj.name if self.interval_obj is not None else None}"

    def harmonize(self, note):
        self.notes[self.cp] = note
        self.interval_obj = interval.Interval(self.notes[0], self.notes[1])
        self.intervalClass = self.interval_obj.intervalClass

if __name__ == '__main__':
    cantus_firmus = 1

    s = converter.parse(fn1)
    sw = ScoreWrapper(s, cantus_firmus)

    # harmony
    s2 = converter.parse(fn2)
    harmony = []
    for n in s2.recurse().getElementsByClass(note.Note):
        harmony.append(n)
    for i in range(0, len(sw.interval_wrappers)):
        sw.interval_wrappers[i].harmonize(harmony[i])
        print(sw.interval_wrappers[i])



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