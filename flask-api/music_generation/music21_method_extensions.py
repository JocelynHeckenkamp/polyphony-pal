import music21

def higherThan(self, note):
    i = music21.interval.Interval(note, self)
    return i.semitones > 0

def lessThan(self, note):
    i = music21.interval.Interval(note, self)
    return i.semitones < 0

def extend():
    music21.note.Note.higherThan = higherThan
    music21.note.Note.lessThan = lessThan
