import music21 as m21
from . import counterpoint_parser as cpp
from . import music21_method_extensions as m21me

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

def check_counterpoint(sw: cpp.ScoreWrapper):
    m21me.extend()

    # if (rule3(sw) # begin with unison
    #     or rule4(sw) # end with unison
    #     or rule5(sw) # closes with contrary motion
    # ):
    #     return True

    for iw in sw.interval_wrappers:
        if (#rule1(iw) # range
            #or rule2(iw) # consonant intervals
            #or rule6(iw) # approaching perfect intervals
            #or rule7(iw) # hidden perfect intervals
            #or rule8(iw) # voice crossing
            #or rule9(iw) # repeated notes melodic intervals
            rule10(iw) # consecutive leaps
        ):
            return True

    return False

def rule1(iw: cpp.IntervalWrapper): # ranges
    mel = iw.notes[1]
    har = iw.notes[0]

    if (mel.higherThan(m21.note.Note(ranges[1][1])) or
        mel.lessThan(m21.note.Note(ranges[1][0])) or
        har.higherThan(m21.note.Note(ranges[0][1])) or
        har.lessThan(m21.note.Note(ranges[0][0]))):

        return True

    return False

def rule2(iw: cpp.IntervalWrapper): # consonant harmonic intervals
    if iw.interval_obj.name not in consonant_intervals:
        return True
    return False

def rule3(sw: cpp.ScoreWrapper): # begin with unison
    if sw.interval_wrappers[0].interval_obj.name not in ["P1", "P8", "P15", "P22"]:
        return True
    return False

def rule4(sw: cpp.ScoreWrapper): # end with unison
    if sw.interval_wrappers[len(sw.interval_wrappers)-1].interval_obj.name not in ["P1", "P8", "P15", "P22"]:
        return True
    return False

def rule5(sw: cpp.ScoreWrapper): # closing
    pen = sw.interval_wrappers[len(sw.interval_wrappers)-2]
    return pen.vlq.closesIncorrectly()

def rule6(iw: cpp.IntervalWrapper): # approaching perfect intervals
    if (iw.prev is not None and iw.interval_obj.name[0] == "P" and not iw.prev.vlq.contraryMotion()):
        return True
    return False

def rule7(iw: cpp.IntervalWrapper): # hidden perfect intervals
    if iw.next is not None:
        if iw.vlq.hiddenFifth() or iw.vlq.hiddenOctave():
            print(iw)
            return True
    return False

def rule8(iw: cpp.IntervalWrapper):
    if iw.notes[0].higherThan(iw.notes[1]):
        return True
    return False

def rule9(iw: cpp.IntervalWrapper): # no repeated notes or unacceptable melodic intervals
    acceptable_leaps = ["m2", "M2", "m3", "M3", "P4", "P5", "m6", "P8"]
    if iw.next is not None:
        if iw.melodic_intervals[0].name not in acceptable_leaps or iw.melodic_intervals[1].name not in acceptable_leaps:
            return True
    return False

def rule10(iw: cpp.IntervalWrapper): # consecutive leaps
    if iw.next is not None and iw.next.next is not None:
        for mi in range(len(iw.melodic_intervals)-1):
            if not iw.melodic_intervals[mi].isStep and not iw.next.melodic_intervals[mi].isStep:
                n1 = iw.notes[mi]
                n2 = iw.next.notes[mi]
                n3 = iw.next.next.notes[mi]
                c = m21.chord.Chord([n1, n2, n3])
                if not c.isTriad() or iw.melodic_intervals[mi].direction != iw.next.melodic_intervals[mi].direction:
                    return True
    return False

if __name__ == '__main__':


    print()