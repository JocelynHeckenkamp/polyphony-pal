import error as e
import music_xml_parser as mxp
WHOLE_CHORD = [True, True, True, True]

# Parse chorddatas and check rules
def check_rules_14_to_26(chord: mxp.ChordWrapper, score: mxp.ScoreWrapper):
    errors = []
    # 14
    # Leadingtones counter := 0
    # foreach note in notes:
    #     if note == four of key or note == seven of key:
    #         Leadingtones counter += 1
    # if Leadingtones counter > 2
    #     Mark "Never double the leading tone" error (voice # & #)


    # 15
    if (chord.inversion == 0 
        and str(chord.quality) != "diminished" 
        and not chord.isSeventh):

        root_counter = 0
        for note in chord.notes:
            if chord.chord_obj.root().name == note.name:
                root_counter += 1
        if root_counter < 2:
            ErrorParams = {
                'title': 'Rule 15',
                'location': chord.location,
                'description': "Rule 15: In root position non-diminished triads, double the root.",
                'suggestion': f'double the root: {chord.chord_obj.root().name}',
                'voices': WHOLE_CHORD,
                'duration': 1.0,
            }
            errors.append(e.Error(**ErrorParams))


    # 16
    if str(chord.quality) == "diminished" and not chord.isSeventh:

        third_counter = 0
        for note in chord.notes:
            if chord.chord_obj.third.name == note.name:
                third_counter += 1
        if third_counter < 2:
            ErrorParams = {
                'title': 'Rule 16',
                'location': chord.location,
                'description': "Rule 16: In diminished triads, double the 3rd (not a value in the tritone).",
                'suggestion': f'double the third: {chord.chord_obj.third.name}',
                'voices': WHOLE_CHORD,
                'duration': 1.0,
            }
            errors.append(e.Error(**ErrorParams))


    # 17
    if (chord.next is not None 
        and str(chord.rn) == "V" 
        and str(chord.next.rn) == "VI" 
        and not chord.next.isSeventh 
        and str(score.key)[-5:] == "minor"):

        third_counter = 0
        for note in chord.next.notes:
            if chord.next.chord_obj.third.name == note.name:
                third_counter += 1
        if third_counter < 2:
            ErrorParams = {
                'title': 'Rule 17',
                'location': chord.location,
                'description': "Rule 17: In the Deceptive Progression (V to VI in minor keys), double the 3rd of the VI chord.",
                'suggestion': f'double the third: {chord.next.chord_obj.third.name}',
                'voices': WHOLE_CHORD,
                'duration': 2.0,
            }
            errors.append(e.Error(**ErrorParams))


    # 18
    if (chord.inversion == 1 
        and chord.quality != "diminished" 
        and not chord.isSeventh):

        bass_note = chord.notes[3].name
        bass_counter = 0
        voices = [False, False, False, False]
        for i, note in enumerate(chord.notes):
            if bass_note == note.name:
                bass_counter += 1
                voices[i] = True
        if bass_counter > 1:
            ErrorParams = {
                'title': 'Rule 18',
                'location': chord.location,
                'description': "Rule 18: In a first inversion non-diminished triads, do not double the bass note.",
                'suggestion': f'do not double the bass note: {bass_note}',
                'voices': voices,
                'duration': 1.0,
            }
            errors.append(e.Error(**ErrorParams))


    # 19
    if (chord.inversion == 2 
        and chord.quality != "diminished" 
        and not chord.isSeventh):

        bass_note = chord.notes[3].name
        bass_counter = 0
        for note in chord.notes:
            if bass_note == note.name:
                bass_counter += 1
        if bass_counter < 2:
            ErrorParams = {
                'title': 'Rule 19',
                'location': chord.location,
                'description': "Rule 19: In second inversion non-diminished triads, double the bass.",
                'suggestion': f'double the bass note: {bass_note}',
                'voices': WHOLE_CHORD,
                'duration': 1.0,
            }
            errors.append(e.Error(**ErrorParams))


    # 20
    if chord.inversion == 2:

        fifth_counter = 0
        for note in chord.notes:
            if chord.chord_obj.fifth.name == note.name:
                fifth_counter += 1
        if fifth_counter < 2:
            ErrorParams = {
                'title': 'Rule 20',
                'location': chord.location,
                'description': "Rule 20: In second inversion, double the 5th (bass note)",
                'suggestion': f'double the 5th: {chord.chord_obj.fifth.name}',
                'voices': WHOLE_CHORD,
                'duration': 1.0,
            }
            errors.append(e.Error(**ErrorParams))
    

    # 21 
    if (chord.next is not None 
        and str(chord.rn) == "IIb" 
        and chord.inversion == 1):

        bass_note = chord.notes[3].name
        bass_counter = 0
        for note in chord.notes:
            if bass_note == note.name:
                bass_counter += 1
        if bass_counter < 2:
            ErrorParams = {
                'title': 'Rule 21',
                'location': chord.location,
                'description': "Rule 21: In a Neapolitan chord, double the bass",
                'suggestion': f'double the bass: {bass_note}',
                'voices': WHOLE_CHORD,
                'duration': 1.0,
            }
            errors.append(e.Error(**ErrorParams))
        if chord.melodic_intervals[2].direction == "Direction.ASCENDING":
            ErrorParams = {
                'title': 'Rule 21',
                'location': chord.location,
                'description': "Rule 21: In a Neapolitan chord, resolve b2^ down to the nearest note of the next chord",
                'suggestion': f'resolve b2^ note down: {chord.notes[2].name}',
                'voices': [False, False, True, False],
                'duration': 2.0,
            }
            errors.append(e.Error(**ErrorParams))
    

    # 22 
    if chord.incomplete and not chord.isSeventh:

        root_counter = 0
        voices = [False, False, False, False]
        for i, note in enumerate(chord.notes):
            if chord.chord_obj.root().name == note.name:
                root_counter += 1
            if chord.chord_obj.fifth is not None:
                voices[i] = True
                ErrorParams = {
                    'title': 'Rule 22',
                    'location': chord.location,
                    'description': "Rule 22: In incomplete triads, omit the 5th",
                    'suggestion': f'Omit the 5th: {note.name}',
                    'voices': voices,
                    'duration': 1.0,
                }
                errors.append(e.Error(**ErrorParams))
        if root_counter < 3:
            ErrorParams = {
                'title': 'Rule 22',
                'location': chord.location,
                'description': "Rule 22: In incomplete triads, triple the root",
                'suggestion': f'Triple the root: {chord.chord_obj.root().name}',
                'voices': WHOLE_CHORD,
                'duration': 1.0,
            }
            errors.append(e.Error(**ErrorParams))   


    # 23
    if chord.incomplete and chord.isSeventh:

        root_counter = 0
        voices = [False, False, False, False]
        for i, note in enumerate(chord.notes):
            if chord.chord_obj.root().name == note.name:
                root_counter += 1
            if chord.chord_obj.fifth is not None:
                voices[i] = True
                ErrorParams = {
                    'title': 'Rule 23',
                    'location': chord.location,
                    'description': "Rule 23: In incomplete 7th chords, omit the 5th",
                    'suggestion': f'Omit the 5th: {note.name}',
                    'voices': voices,
                    'duration': 1.0,
                }
                errors.append(e.Error(**ErrorParams))
        if root_counter < 2:
            ErrorParams = {
                'title': 'Rule 23',
                'location': chord.location,
                'description': "Rule 23: In incomplete 7th chords, double the root",
                'suggestion': f'Double the root: {chord.chord_obj.root().name}',
                'voices': WHOLE_CHORD,
                'duration': 1.0,
            }
            errors.append(e.Error(**ErrorParams))  
 

    # 24
    if (chord.next is not None 
        and str(chord.rn) == "V" 
        and str(chord.next.rn) == "VI" 
        and not chord.next.isSeventh 
        and str(score.key)[-5:] == "minor"):

        voices = [False] * 4
        for i, note in enumerate(chord.notes):
            if note.name == chord.chord_obj.third.name:
                voices[i] = True
                if chord.melodic_intervals[2].direction != "Direction.ASCENDING":
                    ErrorParams = {
                        'title': 'Rule 24',
                        'location': chord.location,
                        'description': "Rule 24: In the Deceptive Progression (V to VI in minor keys), the 3rd of V must resolve up",
                        'suggestion': f'3rd of V must resolve up: {note.name}',
                        'voices': voices,
                        'duration': 2.0,
                    }
                    errors.append(e.Error(**ErrorParams))  
                    

    # 25
    # ***pass in two chords next and curr into this function***
    # if curr.quality == augmented and curr.numeral == VI:
    #     sharp_four := sharp four from key
    #     target index := 0
    #     foreach i, note in enumerate(curr.notes):
    #         if note == sharp four:
    #             target index := i
    #     if next.numeral == V7 and next.notes[target index] != four of key:
    #         Mark "The #4^ of an augmented 6th chord must resolve to 5^ unless the chord resolves to V7 in which case it resolves to natural 4" error (whole chord)
    #     else if next.notes[target index] != five of key:
    #         Mark "The #4^ of an augmented 6th chord must resolve to 5^ unless the chord resolves to V7 in which case it resolves to natural 4" error (whole chord)


    # 26
    if (chord.inversion == 2 
        and not chord.isSeventh 
        and not cadential64(chord) 
        and not passingInBass(chord) 
        and not pedalPoint(chord)):

        ErrorParams = {
            'title': 'Rule 26',
            'location': chord.location,
            'description': "Rule 26: 6/4 Chords can only be used in four cases: cadential 6/4, passing in bass, arpeggio staying on same chord, pedal point",
            'suggestion': f'6/4 Chords can only be used in four cases: cadential 6/4, passing in bass, arpeggio staying on same chord, pedal point',
            'voices': WHOLE_CHORD,
            'duration': 1.0,
        }
        errors.append(e.Error(**ErrorParams))  

    return errors


def cadential64(chord: mxp.ChordWrapper):
    return (chord.next is not None 
            and chord.next.next is not None 
            and (str(chord.next.rn) == "V") # can be normal or seventh chord 
            and str(chord.next.next.rn) == "I")


def passingInBass(chord: mxp.ChordWrapper):
    return (chord.prev is not None                                                          # ensure previous chord exists 
            and chord.next is not None                                                      # ensure next chord exists
            and str(chord.prev.melodic_intervals[3].name)[1] == "2"                        # ensure stepwise motion btween prev and curr chords
            and str(chord.melodic_intervals[3].name)[1] == "2"                             # ensure stepwise motion btween curr and next chords
            and chord.prev.melodic_intervals[3].direction == chord.harmonic_intervals[3])  # ensure motion is in the same direction


def pedalPoint(chord: mxp.ChordWrapper):
    return (chord.prev is not None                                                          # ensure previous chord exists
            and chord.next is not None                                                      # ensure next chord exists
            and chord.prev.notes[3] is chord.notes[3]                                       # ensure previous bass is the same as current bass
            and chord.notes[3] is chord.next.notes[3])                                      # ensure current bass is the same as next bass
    