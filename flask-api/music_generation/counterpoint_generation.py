from . import counterpoint_parser as cpp
from . import counterpoint_rules as cpr
from . import music21_method_extensions as m21me
from music21 import *

verbose = False

def generate_counterpoint(fn, cantus_firmus):
    m21me.extend()

    sw = cpp.getScoreWrapper(fn, cantus_firmus)

    correct_counterpoints = []
    tree_indices = [0] * len(sw.interval_wrappers)

    mm = 0
    count = 0
    while mm < len(sw.interval_wrappers):
        if verbose: print(mm)
        if tree_indices[mm] == len(sw.interval_wrappers[mm].counterpoints):
            if verbose: print("Exausted level", mm, "with", tree_indices)
            if mm == 0:
                print("Parsing complete")
                if verbose: print(correct_counterpoints)
                break
            for i in range(mm, len(tree_indices)):
                tree_indices[i] = 0
            tree_indices[mm-1] += 1
            mm -= 1
            continue

        cp = sw.interval_wrappers[mm].counterpoints[tree_indices[mm]]
        sw.interval_wrappers[mm].harmonize(note.Note(cp))

        if mm > 0:
            sw.calc_vlqs(mm-1)

        # rules
        if verbose: print("Testing ", cp)
        passing = True

        iw = sw.interval_wrappers[mm]

        if (cpr.rule1(iw) or cpr.rule2(iw) or cpr.rule8(iw)):
            passing = False

        if mm > 0:
            if (cpr.rule6(iw) or cpr.rule7(iw.prev) or cpr.rule9(iw.prev) or cpr.rule11(iw.prev)):
                passing = False

        if mm > 1:
            if (cpr.rule10(iw.prev.prev) or cpr.rule12(iw.prev.prev)):
                passing = False

        if mm == len(sw.interval_wrappers)-1:
            if (cpr.rule4(sw) or cpr.rule5(sw)):
                passing = False

        # handle passing
        if verbose and passing:
            print("Pass", mm, ":", cp)

        if not passing:
            if verbose: print("Fail", mm, ":", cp)
            tree_indices[mm] += 1
            mm -= 1

        if mm == len(sw.interval_wrappers)-1:
            counterpoint = []
            count += 1
            for iw in sw.interval_wrappers:
                counterpoint.append(iw.notes[iw.cp])
                iw.reset()
            correct_counterpoints.append(counterpoint)
            print(count, ":", counterpoint)
            tree_indices[-1] += 1
            mm = -1

        mm += 1

    # return correct_counterpoints

    musicXMLs = []

    for cp in correct_counterpoints:
        musicXMLs.append(createXML(sw, cp))

    print(musicXMLs)
    return musicXMLs

def createXML(sw, noteList):
    s = stream.Score()
    partStaves = [stream.PartStaff(instrument.Piano()), stream.PartStaff(instrument.Piano())]
    partStaves[0].clef = clef.BassClef()
    partStaves[1].clef = clef.TrebleClef()

    for mm, iw in enumerate(sw.interval_wrappers):
        measures = [stream.Measure(number=mm, offset=0), stream.Measure(number=mm, offset=0)]
        voices = [stream.Voice(id=1), stream.Voice(id=2)]

        if mm == 0:
            measures[0].insert(0, meter.TimeSignature('4/4'))  # Set time signature
            measures[0].insert(0, sw.key_signature)
            measures[1].insert(0, meter.TimeSignature('4/4'))  # Set time signature
            measures[1].insert(0, sw.key_signature)

        cf = iw.notes[sw.cf]
        cp = noteList[mm]
        cf.duration.type = "whole"
        cp.duration.type = "whole"
        voices[sw.cf].append(cf)
        voices[sw.cp].append(cp)

        measures[0].append(voices[0])
        measures[1].append(voices[1])
        partStaves[0].append(measures[0])
        partStaves[1].append(measures[1])

    s.append(partStaves[1])
    s.append(partStaves[0])

    # s.show()

    # return string
    GEX = musicxml.m21ToXml.GeneralObjectExporter(s)
    out = GEX.parse()
    outStr = out.decode('utf-8')
    return outStr

