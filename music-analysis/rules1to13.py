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
    errors.extend(rule6(chord)) # double melodic leaps
    errors.extend(rule7(chord)) # resolving leaps
    errors.extend(rule8(chord)) # resolving diminished movement
    errors.extend(rule9(chord)) # resolving the seventh of a chord
    errors.extend(rule10(chord)) # non-chords

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

def rule6(chord: mxp.ChordWrapper): # double leaps
    errors = []

    for a in range(len(chord.melodic_intervals)):
        if (int(chord.melodic_intervals[a].name[1]) > 2 and chord.next is not None and chord.next.next is not None):
            if (int(chord.next.melodic_intervals[a].name[1]) > 2):
                melodic_chord = music21.chord.Chord([chord.notes[a], chord.next.notes[a], chord.next.next.notes[a]])
                if (melodic_chord.isTriad and not (melodic_chord.isIncompleteMajorTriad or melodic_chord.isIncompleteMinorTriad)):
                    voices = [False] * 4
                    voices[a] = True
                    ErrorParams = {
                        'title': "Double Melodic Leap not a Triad",
                        'location': chord.location,
                        'description': f"{voice_names[a]} leaps twice not outlining a triad.",
                        'suggestion': "Change a leap to a step.",
                        'voices': voices,
                        'duration': 3.0,
                    }
                    errors.append(e.Error(**ErrorParams))

    return errors

def rule7(chord: mxp.ChordWrapper): # resolving leaps
    errors = []

    for a in range(len(chord.melodic_intervals)):
        i = chord.melodic_intervals[a]
        if (int(i.name[1]) > 4 and chord.next is not None and chord.next.next is not None):
            i2 = chord.next.melodic_intervals[a]
            if (not (i2.isStep and i.diatonic.direction != i2.diatonic.direction)):
                voices = [False] * 4
                voices[a] = True
                ErrorParams = {
                    'title': "Improperly Resolved Leap",
                    'location': chord.location,
                    'description': f"{voice_names[a]} leaps greater than P4 without resolve.",
                    'suggestion': "Resolve stepwise in the opposite direction.",
                    'voices': voices,
                    'duration': 3.0,
                }
                errors.append(e.Error(**ErrorParams))

    return errors

def rule8(chord: mxp.ChordWrapper): # resolving diminished movement
    errors = []

    for a in range(len(chord.melodic_intervals)):
        i = chord.melodic_intervals[a]
        if (i.name[0] == 'd' and chord.next is not None and chord.next.next is not None):
            i2 = chord.next.melodic_intervals[a]
            if (not (i2.isStep and i.diatonic.direction != i2.diatonic.direction)):
                voices = [False] * 4
                voices[a] = True
                ErrorParams = {
                    'title': "Improperly Resolved Leap",
                    'location': chord.location,
                    'description': f"{voice_names[a]} moves by diminished interval without resolving.",
                    'suggestion': "Resolve stepwise in the opposite direction.",
                    'voices': voices,
                    'duration': 3.0,
                }
                errors.append(e.Error(**ErrorParams))

    return errors

def rule9(chord: mxp.ChordWrapper): # resolving the 7th
    errors = []

    for a in range(len(chord.notes)):
        if (chord.notes[a].pitch == chord.chord_obj.seventh): # note is seventh
            if (chord.next is None or
                (not chord.melodic_intervals[a].isStep
                or chord.prev is not None and chord.prev.melodic_intervals[a].direction != chord.melodic_intervals[a].direction)):

                # conditions to skip
                if (a != 0 # seventh is not in soprano
                    and (chord.rn == 'i' or chord.rn == 1) # cadential 6/4
                    and chord.inversion == 2
                    and chord.next is not None
                    and (chord.next.rn == 'v' or chord.next.rn == 5)
                    and (chord.next[a].pitch == chord.chord_obj.getChordStep(5))):
                    continue;

                voices = [False] * 4
                voices[a] = True
                ErrorParams = {
                    'title': "Improperly Resolved Seventh",
                    'location': chord.location,
                    'description': f"Seventh {voice_names_lower[a]} does not resolve stepwise in opposite direction.",
                    'suggestion': "Resolve stepwise in the opposite direction.",
                    'voices': voices,
                    'duration': 2.0,
                }
                errors.append(e.Error(**ErrorParams))

    return errors

# test for augented sixth chords
def rule10(chord: mxp.ChordWrapper): # resolving the 7th
    errors = []

    co = chord.chord_obj
    if (not (co.isTriad == True or co.isSeventh == True)):
        voices = [True] * 4
        ErrorParams = {
            'title': "Impermissable Chord Type",
            'location': chord.location,
            'description': f"Voices do not form a triad or seventh chord.",
            'suggestion': "Rewrite as a seventh chord or triad.",
            'voices': voices,
            'duration': 2.0,
        }
        errors.append(e.Error(**ErrorParams))

    return errors

if __name__ == '__main__':
    #fn = "../music-xml-examples/bad-voice-leading-2.musicxml"
    fn = "../music-xml-examples/rule-10-test.musicxml"
    sw = mxp.getScoreWrapper(fn)
    curr = sw.chord_wrappers[0]
    errors = []
    while (curr is not None):
        #print(curr, curr.inversion)
        errors.extend(check_rules_1_to_13(curr, sw))
        for error in errors:
            print(error)
        curr = curr.next