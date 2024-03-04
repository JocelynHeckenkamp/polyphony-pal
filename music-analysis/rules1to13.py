import error as e
import music21
import music_xml_parser as mxp
WHOLE_CHORD = [True, True, True, True]


# Parse chorddatas and check rules
def check_rules_1_to_13(chord: mxp.ChordWrapper, score: mxp.ScoreWrapper):
    music21.note.Note.higherThan = higherThan
    music21.note.Note.lessThan = lessThan

    errors = []

    errors.extend(rule1(chord, score)) # range

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

def higherThan(self, note):
    i = music21.interval.Interval(note, self)
    return i.semitones > 0

def lessThan(self, note):
    i = music21.interval.Interval(note, self)
    return i.semitones < 0

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
            and chord.notes[3] is chord.next.notes[3])

# rule 1: range
def rule1(chord: mxp.ChordWrapper, score: mxp.ScoreWrapper):
    errors = []
    ranges = [
        ('C4', 'G5'),  # soprano
        ('G3', 'C5'),  # alto
        ('C3', 'G4'),  # tenor
        ('E2', 'C4')  # bass
    ]
    voice_names = ["Soprano", "Alto", "Tenor", "Bass"]
    for i in range(len(ranges)):
        n = chord.notes[i]
        if n.higherThan(music21.note.Note(ranges[i][1])) or n.lessThan(music21.note.Note(ranges[i][0])):
            low, high = ranges[i]
            voice_name = voice_names[i]
            voices = [False] * 4
            voices[i] = True
            ErrorParams = {
                'title': "Range Error",
                'location': chord.location,
                'description': f"{voice_name} is out of range.",
                'suggestion': f"Write voice in range [{low}, {high}].",
                'voices': voices,
                'duration': 0.0,
            }
            errors.append(e.Error(**ErrorParams))

    return errors

if __name__ == '__main__':
    fn = "../music-xml-examples/voice-leading-1.musicxml"
    sw = mxp.getScoreWrapper(fn)
    curr = sw.chord_wrappers[0]
    errors = []
    while (curr is not None):
        #print(curr, curr.inversion)
        errors.extend(check_rules_1_to_13(curr, sw))
        for error in errors:
            print(error)
        curr = curr.next