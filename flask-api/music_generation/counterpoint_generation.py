from . import counterpoint_parser as cpp
from . import counterpoint_rules as cpr
from . import music21_method_extensions as m21me
import music21 as m21

def generate_counterpoint(fn, cantus_firmus):
    m21me.extend()

    sw = cpp.getScoreWrapper(fn, cantus_firmus)

    correct_counterpoints = []
    tree_indices = [0] * len(sw.interval_wrappers)

    #for mm in range(len(sw.interval_wrappers)):
    mm = 0
    while mm < len(sw.interval_wrappers):
        print(mm)
        if tree_indices[mm] == len(sw.interval_wrappers[mm].counterpoints):
            print("Exausted level", mm, "with", tree_indices)
            if mm == 0:
                print("Parsing complete")
                break
            for i in range(mm, len(tree_indices)):
                tree_indices[i] = 0
            tree_indices[mm-1] += 1
            mm -= 1
            continue

        cp = sw.interval_wrappers[mm].counterpoints[tree_indices[mm]]
        sw.interval_wrappers[mm].harmonize(m21.note.Note(cp))

        if mm > 0:
            sw.calc_vlqs(mm-1)

        # rules
        print("Testing ", cp)
        passing = True
        #for i in range(0, mm+1):

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
        if passing:
            print("Pass", mm, ":", cp)

        if not passing:
            print("Fail", mm, ":", cp)
            tree_indices[mm] += 1
            mm -= 1

        # completed one
        # save value
        # reset harmonizations
        # increment last tree index
        # reset mm
        # remember to handle errors in sliding window above (or do I not have to?)

        if mm == len(sw.interval_wrappers)-1:
            counterpoint = []
            for iw in sw.interval_wrappers:
                counterpoint.append(iw.notes[iw.cp])
                iw.reset()
            print(counterpoint)

        mm += 1


    print(tree_indices)

    print()