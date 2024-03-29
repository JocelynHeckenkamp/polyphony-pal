import music21
from . import music_xml_parser

def higherThan(self, note):
    i = music21.interval.Interval(note, self)
    return i.semitones > 0

def lessThan(self, note):
    i = music21.interval.Interval(note, self)
    return i.semitones < 0

def indicesOfNote(self, note):
    indices = []
    for a in range(len(self.notes)):
        if (self.notes[a].name == note.name):
            indices.append(a)
    return indices

def indicesOfDegree(self, d, key):
    return self.indicesOfNote(key.pitchFromDegree(d))

def degreeResolvesTo(self, d1, d2, key):
    if self.next is None:
        return False

    voices = self.indicesOfDegree(d1, key)
    if not voices: # empty list; chord doesn't contain note
        return True

    for voice in voices:
        if not self.next.notes[voice].name == key.pitchFromDegree(d2).name:
            return False

    return True

def degreeResolvesToByStep(self, d1, d2, key):

    if self.next is None:
        return False

    voices = self.indicesOfDegree(d1, key)
    if not voices: # empty list; chord doesn't contain note
        return True

    for voice in voices:
        if not (self.next.notes[voice].name == key.pitchFromDegree(d2).name or self.melodic_intervals[voice].isStep):
            return False

    return True

def extend():
    music21.note.Note.higherThan = higherThan
    music21.note.Note.lessThan = lessThan
    music_xml_parser.ChordWrapper.indicesOfNote = indicesOfNote
    music_xml_parser.ChordWrapper.indicesOfDegree = indicesOfDegree
    music_xml_parser.ChordWrapper.degreeResolvesTo = degreeResolvesTo
    music_xml_parser.ChordWrapper.degreeResolvesToByStep = degreeResolvesToByStep
