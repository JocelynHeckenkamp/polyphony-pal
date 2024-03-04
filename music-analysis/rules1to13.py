import error as e
import music21
import music_xml_parser as mxp
WHOLE_CHORD = [True, True, True, True]
voice_names = ["Soprano", "Alto", "Tenor", "Bass"]
voice_names_lower = ["soprano", "alto", "tenor", "bass"]


# Parse chorddatas and check rules
def check_rules_1_to_13(chord: mxp.ChordWrapper, score: mxp.ScoreWrapper):
    music21.note.Note.higherThan = higherThan
    music21.note.Note.lessThan = lessThan

    errors = []

    errors.extend(rule1(chord)) # range
    errors.extend(rule2(chord)) # spacing
    errors.extend(rule3(chord)) # voice crossing
    errors.extend(rule4(chord)) # voice overlapping
    errors.extend(rule5(chord)) # large melodic leaps

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

def rule1(chord: mxp.ChordWrapper): # range
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
                'duration': 1.0,
            }
            errors.append(e.Error(**ErrorParams))

    return errors

def rule2(chord: mxp.ChordWrapper): # spacing
    errors = []

    s_a = chord.harmonic_intervals[(0, 1)]
    a_t = chord.harmonic_intervals[(1, 2)]

    title = "Spacing Error"

    if s_a.semitones > 12:
        ErrorParams = {
            'title': title,
            'location': chord.location,
            'description': "Soprano and alto voices are wider than P8.",
            'suggestion': "Lower the soprano voice or raise the alto voice.",
            'voices': [True, True, False, False],
            'duration': 1.0,
        }
        errors.append(e.Error(**ErrorParams))

    if a_t.semitones > 12:
        ErrorParams = {
            'title': title,
            'location': chord.location,
            'description': "Alto and tenor voices are wider than P8.",
            'suggestion': "Lower the alto voice or raise the tenor voice.",
            'voices': [False, True, True, False],
            'duration': 1.0,
        }
        errors.append(e.Error(**ErrorParams))

    return errors

def rule3(chord: mxp.ChordWrapper): # voice crossing
    errors = []

    for a in range(len(chord.notes)-1):
        for b in range(a, len(chord.notes)):
            if chord.notes[b].higherThan(chord.notes[a]):
                voices = [False] * 4
                voices[a] = True
                voices[b] = True
                ErrorParams = {
                    'title': "Voice Crossing",
                    'location': chord.location,
                    'description': f"{voice_names[b]} voice is above {voice_names_lower[a]} voice.",
                    'suggestion': "Move or switch voices.",
                    'voices': voices,
                    'duration': 1.0,
                }
                errors.append(e.Error(**ErrorParams))

    return errors

def rule4(chord: mxp.ChordWrapper): # overlapping
    errors = []

    title = "Voice Overlapping"

    for a in range(len(chord.notes)-1):
        if chord.next is not None and chord.notes[a].lessThan(chord.next.notes[a+1]):
            voices = [False] * 4
            voices[a] = True
            voices[a+1] = True
            ErrorParams = {
                'title': "Voice Overlapping",
                'location': chord.location,
                'description': f"{voice_names[a+1]} crosses above the {voice_names_lower[a]} voice.",
                'suggestion': "",
                'voices': voices,
                'duration': 2.0,
            }
            errors.append(e.Error(**ErrorParams))

    return errors

def rule5(chord: mxp.ChordWrapper): # melodic leaps
    errors = []

    for a in range(len(chord.melodic_intervals)):
        if chord.melodic_intervals[a].semitones > 12:
            voices = [False] * 4
            voices[a] = True
            ErrorParams = {
                'title': "Large Melodic Leap",
                'location': chord.location,
                'description': f"{voice_names[a]} leaps an interval greater than P8.",
                'suggestion': "",
                'voices': voices,
                'duration': 2.0,
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