from . import error as e
import music21
from . import music_xml_parser as mxp
from . import music21_method_extensions
WHOLE_CHORD = [True, True, True, True]
voice_names = ["Soprano", "Alto", "Tenor", "Bass"]
voice_names_lower = ["soprano", "alto", "tenor", "bass"]

def check_rules_25_28to31(chord: mxp.ChordWrapper, score: mxp.ScoreWrapper):
    music21_method_extensions.extend()

    all_errors = []

    all_errors.extend(rule25(chord, score))     # curr, next & last | resolving augmented sixth chords
    all_errors.extend(rule28(chord))            # last | cadences
    all_errors.extend(rule29(chord, score))     # curr, next & last | resolving V7
    all_errors.extend(rule30(chord, score))     # curr, next & last | resolving (half) diminished seventh chords
    all_errors.extend(rule31(chord))            # curr, next | augmented melodic intervals

    return all_errors

def rule25(chord: mxp.ChordWrapper, sw):
    errors = []
    if chord.chord_obj.isAugmentedSixth():
        #print(chord)
        link = "https://musictheory.pugetsound.edu/mt21c/VoiceLeadingAugmentedSixthChords.html"
        if chord.next is None:
            ErrorParams = {
                'title': "Unresolved Augmented 6th Chord",
                'location': chord.location,
                'description': f"Augmented 6th chord does not resolve",
                'suggestion': "Do not end on an augmented sixth chord.",
                'voices': [True] * 4,
                'duration': 1.0,
                'link': link
            }
            errors.append(e.Error(**ErrorParams))
        elif not (chord.next.rn.romanNumeralAlone == "V" or (chord.next.rn.romanNumeralAlone.lower() == "i" and chord.next.inversion == 2)):
            ErrorParams = {
                'title': "Unresolved Augmented 6th Chord",
                'location': chord.location,
                'description': f"Augmented 6th chord must resolve to i64, I64, V, or V7.",
                'suggestion': f"Change {chord.next.rn.romanNumeralAlone} chord to i64, I64, V, or V7.",
                'voices': [True] * 4,
                'duration': 2.0,
                'link': link
            }
            errors.append(e.Error(**ErrorParams))
        else:
            s4 = sw.key.pitchFromDegree(4).transpose("A1")
            aug_4th_indices = chord.indicesOfNote(s4)
            for i in aug_4th_indices:
                if (chord.next.rn.romanNumeralAlone == "V" and chord.next.chord_obj.isDominantSeventh()):
                    if chord.next.notes[i].name != sw.key.pitchFromDegree(4):
                        ErrorParams = {
                            'title': "Improperly Resolved Augmented 6th Chord",
                            'location': chord.location,
                            'description': f"#4 in augmented 6th chord must resolve to degree 4 in V7 or 5 in i64 or I64.",
                            'suggestion': f"Resolve {s4.name} in {voice_names_lower[i]} to {sw.key.pitchFromDegree(4).name}.",
                            'voices': [True] * 4,
                            'duration': 2.0,
                            'link': link
                        }
                        errors.append(e.Error(**ErrorParams))
                elif (chord.next.rn.romanNumeralAlone == "i" or chord.next.rn.romanNumeralAlone == "I"):
                    if chord.next.notes[i].name != sw.key.pitchFromDegree(5):
                        ErrorParams = {
                            'title': "Improperly Resolved Augmented 6th Chord",
                            'location': chord.location,
                            'description': f"#4 in augmented 6th chord must resolve to degree 4 in V7 or 5 in i64 or I64.",
                            'suggestion': f"Resolve {s4.name} in {voice_names_lower[i]} to {sw.key.pitchFromDegree(5).name}.",
                            'voices': [True] * 4,
                            'duration': 2.0,
                            'link': link
                        }
                        errors.append(e.Error(**ErrorParams))

    return errors

def rule28(chord: mxp.ChordWrapper): # cadences
    errors = []

    if (chord.next is None and chord.prev is not None):
        pen_rn = chord.prev.rn.scaleDegree
        last_rn = chord.rn.scaleDegree

        if (not (pen_rn == 5 and (last_rn == 1 or last_rn == 6) # PAC, IAC, Deceptive
                or (pen_rn == 4 and last_rn == 1) # Plagal
                or last_rn == 5)): # Half
            voices = [False] * 4
            ErrorParams = {
                'title': "Improper Cadence",
                'location': chord.location,
                'description': f"No proper cadence.",
                'suggestion': "Rewrite last two chords with authentic cadence, plagal cadence, or deceptive cadence.",
                'voices': voices,
                'duration': 2.0,
                'link': "https://musictheory.pugetsound.edu/mt21c/cadences.html"
            }
            errors.append(e.Error(**ErrorParams))

    return errors

def rule29(chord: mxp.ChordWrapper, sw): # resolving V7
    errors = []

    link = "https://musictheory.pugetsound.edu/mt21c/V7toIVoiceLeading.html"
    if (chord.rn.romanNumeralAlone == "V" and chord.chord_obj.isDominantSeventh()): #V7
        if chord.next is None: # ending on V7
            ErrorParams = {
                'title': "Unresolved V7",
                'location': chord.location,
                'description': f"V7 does not resolve.",
                'suggestion': "Resolve V7 or change it to another chord.",
                'voices': [True] * 4,
                'duration': 1.0,
                'link': link
            }
            errors.append(e.Error(**ErrorParams))
        elif chord.next.rn.scaleDegree != 1:
            ErrorParams = {
                'title': "Unresolved V7",
                'location': chord.location,
                'description': f"V7 does not resolve to I or i.",
                'suggestion': "Resolve to I or i, or the change V7 to another chord.",
                'voices': [True] * 4,
                'duration': 2.0,
                'link': link
            }
            errors.append(e.Error(**ErrorParams))
        else:
            hasError = False

            suggestion = ""
            voices = [False] * 4

            lt1 = chord.degreeResolvesToByStep(7, 1, sw.key)
            lt5xs = chord.degreeResolvesTo(7, 5, sw.key) and chord.indicesOfDegree(7, sw.key)[0] != 0
            if not (lt1 or lt5xs):
                hasError = True
                for v in chord.indicesOfDegree(7, sw.key):
                    voices[v] = True
                suggestion += f"Resolve {sw.key.pitchFromDegree(7).name} to {sw.key.pitchFromDegree(1).name} by step (leading tone to tonic), or to {sw.key.pitchFromDegree(5).name} if it's not in the soprano voice.\n"

            if not chord.degreeResolvesTo(2, 1, sw.key):
                hasError = True
                for v in chord.indicesOfDegree(2, sw.key):
                    voices[v] = True
                    suggestion += f"Resolve {sw.key.pitchFromDegree(2).name} in {voice_names_lower[v]} to {sw.key.pitchFromDegree(1).name} by step (scale degree 2 to 1).\n"

            if not chord.degreeResolvesTo(4, 3, sw.key):
                hasError = True
                for v in chord.indicesOfDegree(4, sw.key):
                    voices[v] = True
                    suggestion += f"Resolve {sw.key.pitchFromDegree(4).name} in {voice_names_lower[v]} to {sw.key.pitchFromDegree(3).name} by step (scale degree 4 to 3).\n"

            if hasError:
                ErrorParams = {
                    'title': "Unresolved V7",
                    'location': chord.location,
                    'description': f"V7 is resolved improperly.",
                    'suggestion': suggestion,
                    'voices': voices,
                    'duration': 2.0,
                    'link': link
                }
                errors.append(e.Error(**ErrorParams))

    return errors

def rule30(chord: mxp.ChordWrapper, sw):
    errors = []

    if (chord.chord_obj.isDiminishedSeventh() or chord.chord_obj.isHalfDiminishedSeventh()):

        link = "https://musictheory.pugetsound.edu/mt21c/VoiceLeadingSecondaryChords.html"

        seventhAboveThird = False
        for n in chord.notes:
            if n.name == chord.chord_obj.third.name:
                break
            elif n.name == chord.chord_obj.seventh.name:
                seventhAboveThird = True
                break

        if chord.next is None:
            ErrorParams = {
                'title': "Unresolved Diminished Seventh Chord",
                'location': chord.location,
                'description': f"Diminished seventh chord does  not resolve.",
                'suggestion': "Do not end on a chord of diminished quality.",
                'voices': [True] * 4,
                'duration': 1.0,
                'link': link
            }
            errors.append(e.Error(**ErrorParams))
        elif not (chord.degreeResolvesToByStep(4, 3, sw.key)
                  and chord.degreeResolvesToByStep(6, 5, sw.key)
                  and chord.degreeResolvesToByStep(7, 8, sw.key)
                  and ((chord.degreeResolvesToByStep(2, 1, sw.key) and seventhAboveThird) or (chord.degreeResolvesToByStep(2, 1, sw.key) and not seventhAboveThird))):
            ErrorParams = {
                'title': "Improperly Resolved Diminished Seventh Chord",
                'location': chord.location,
                'description': f"All tendency tones of a diminished seventh chord must resolve properly.",
                'suggestion': f"Resolve scale degrees 4 to 3, 6, to 5, 7 to 8, and 2 to 1 (or to 3 if the 7th is above the 3rd).",
                'voices': [True] * 4,
                'duration': 2.0,
                'link': link
            }
            errors.append(e.Error(**ErrorParams))

    return errors

def rule31(chord: mxp.ChordWrapper):
    errors = []

    for a in range(len(chord.melodic_intervals)):
        if chord.melodic_intervals[a].simpleName[0] == "A":
            voices = [False] * 4
            voices[a] = True
            ErrorParams = {
                'title': "Augmented Melodic Interval",
                'location': chord.location,
                'description': f"Melodic interval of augmented quality",
                'suggestion': "",
                'voices': voices,
                'duration': 2.0,
                'link': "https://musictheory.pugetsound.edu/mt21c/RulesOfMelody.html"
            }
            errors.append(e.Error(**ErrorParams))

    return errors

if __name__ == '__main__':
    #fn = "../music-xml-examples/voice-leading-1.musicxml"
    fn = "../music-xml-examples/rule13.musicxml"
    sw = mxp.getScoreWrapper(fn)
    curr = sw.chord_wrappers[0]
    errors = []
    while (curr is not None):
        errors.extend(check_rules_25_28to31(curr, sw))
        curr = curr.next

    for error in errors:
        print(error)