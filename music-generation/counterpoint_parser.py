from music21 import *
import os

fn = "../../music-xml-examples/counterpoint1.musicxml"

#class ScoreWrapper:

class IntervalWrapper:
    cf = None # cantus firmus index (0 or 1)
    cp = None # counterpoint index (0 or 1)

    notes = [None, None]
    interval_obj = None # interval
    intervalClass = None

    prev = None
    next = None

    #quality = None

    def __init__(self, note, cantus_firmus):
        self.cf = cantus_firmus
        self.cp = not cantus_firmus
        self.notes[self.cf] = note

        print(self.cf)
        print(self.cp)

    def harmonize(self, note, counterpoint_index):
        self.v2 = note
        self.int = interval.Interval(self.v2, self.v1)
        self.intervalClass = self.int.intervalClass

if __name__ == '__main__':
    s = converter.parse(fn)
    print(s)

    for el in s.recurse():
        print(el)

    print("=========")

    for a in s.getElementsByClass(stream.Part):
        for b in a.recurse().getElementsByClass(note.Note):
            print(b)

    print("----------")

    for el in s.recurse().getElementsByClass(note.Note):
        print(el)