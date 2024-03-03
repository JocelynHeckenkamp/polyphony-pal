import error as e
import music_xml_parser as mxp
WHOLE_CHORD = [True, True, True, True]

# Parse chorddatas and check rules
def check_rules_14_to_26(chord: mxp.ChordWrapper, score: mxp.ScoreWrapper):
    errors = []

    # rule 1: ranges

    # rule 2: spacing

    # rule 3: crossing

    # rule 4: overlapping

    # rule 5: leaping once

    # rule 6: leaping twice

    # rule 7: large leaps

    # rule 8: leaps of diminished quality

    # rule 9: resolution of 7^

    # rule 10: chords

    # rule 11: parallel octaves

    # rule 12: parallel 5ths

    # rule 13: hidden 5ths and octaves

    return errors


def cadential64(chord: mxp.ChordWrapper):
    return (chord.next is not None 
            and chord.next.next is not None 
            and (str(chord.next.rn) == "V") # can be normal or seventh chord 
            and str(chord.next.next.rn) == "I")


def passingInBass(chord: mxp.ChordWrapper):
    return (chord.prev is not None                                                          # ensure previous chord exists 
            and chord.next is not None                                                      # ensure next chord exists
            and str(chord.prev.harmonic_intervals[3].name)[1] == "2"                        # ensure stepwise motion btween prev and curr chords
            and str(chord.harmonic_intervals[3].name)[1] == "2"                             # ensure stepwise motion btween curr and next chords
            and chord.prev.harmonic_intervals[3].direction == chord.harmonic_intervals[3])  # ensure motion is in the same direction


def pedalPoint(chord: mxp.ChordWrapper):
    return (chord.prev is not None                                                          # ensure previous chord exists
            and chord.next is not None                                                      # ensure next chord exists
            and chord.prev.notes[3] is chord.notes[3]                                       # ensure previous bass is the same as current bass
            and chord.notes[3] is chord.next.notes[3])                                      # ensure current bass is the same as next bass
    