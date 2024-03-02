import error as e
import music_xml_parser as mxp
WHOLE_CHORD = [True, True, True, True]
# params = {
#     'title': 'dummyError',
#     'location': tuple((1, 0.0)),
#     'description': 'you are being dumb',
#     'suggestion': 'dont be dumb',
#     'voices': [False, True, False, False],
#     'duration': 1.0,
# }
# dummy = e.Error(**params)
# print(dummy)

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
    if chord.inversion == 0 and str(chord.quality) != "diminished" and not chord.isSeventh:
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
            if chord.chord_obj.third().name == note.name:
                third_counter += 1
        if third_counter < 2:
            ErrorParams = {
                'title': 'Rule 16',
                'location': chord.location,
                'description': "Rule 16: In diminished triads, double the 3rd (not a value in the tritone).",
                'suggestion': f'double the third: {chord.chord_obj.third().name}',
                'voices': WHOLE_CHORD,
                'duration': 1.0,
            }
            errors.append(e.Error(**ErrorParams))

    # 17
    if chord.next is not None and str(chord.rn) == "V" and str(chord.next.rn) == "VI" and not chord.next.isSeventh and str(score.key)[-5:] == "minor":
        third_counter = 0
        for note in chord.next.notes:
            if chord.next.chord_obj.third().name == note.name:
                third_counter += 1
        if third_counter < 2:
            ErrorParams = {
                'title': 'Rule 17',
                'location': chord.location,
                'description': "Rule 17: In the Deceptive Progression (V to VI in minor keys), double the 3rd of the VI chord.",
                'suggestion': f'double the third: {chord.next.chord_obj.third().name}',
                'voices': WHOLE_CHORD,
                'duration': 2.0,
            }
            errors.append(e.Error(**ErrorParams))

    # 18
    if chord.inversion == 1 and chord.quality != "diminished" and not chord.isSeventh:
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
    if chord.inversion == 2 and chord.quality != "diminished" and not chord.isSeventh:
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
            if chord.chord_obj.fifth().name == note.name:
                fifth_counter += 1
        if fifth_counter < 2:
            ErrorParams = {
                'title': 'Rule 20',
                'location': chord.location,
                'description': "Rule 20: In second inversion, double the 5th (bass note)",
                'suggestion': f'double the 5th: {chord.chord_obj.fifth().name}',
                'voices': WHOLE_CHORD,
                'duration': 1.0,
            }
            errors.append(e.Error(**ErrorParams))
    

    # 21 
    # if numeral == 'IIb' and inversion == 1:
    #     bass note := notes[3]
    #     bass counter := 0
    #     foreach note in notes:
    #         if note == bass note:
    #             bass counter += 1
    #     if bass counter < 2
    #         Mark "In a Neapolitan chord, double the bass and resolve b2^ down to the nearest note of the next chord" error (whole chord)
    #     if harmonic_interval[2].chromatic_direction > 0:
    #         Mark "In a Neapolitan chord, double the bass and resolve b2^ down to the nearest note of the next chord" error (voice 2)
    #TODO: fix melodic intervals
    if str(chord.rn) == "IIb" and chord.inversion == 1:
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
        if chord.harmonic_intervals[2].direction > 0:
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
    # if incomplete and not 7th-chord:
    #     root counter := 0
    #     foreach note in notes:
    #         if note == chord.root:
    #             root counter += 1
    #         if note == chord.fifth:
    #             Mark "In incomplete triads, triple the root and omit the 5th" error (voice #)
    #     if root counter < 3
    #         Mark "In incomplete triads, triple the root and omit the 5th" error (whole chord)   

    # 23
    # if incomplete and 7th-chord:
    #     root counter := 0
    #     foreach note in notes:
    #         if note == chord.root:
    #             root counter += 1
    #         if note == chord.fifth:
    #             Mark "In incomplete 7th chords, double the root and omit the 5th" error (voice #)
    #     if root counter < 2
    #         Mark "In incomplete 7th chords, double the root and omit the 5th" error (whole chord)  
    # 24
    # ***pass in two chords prev and curr into this function***
    # if prev.numeral == V and curr.numeral == VI and not curr.7th-chord and key.quality == minor:
    #     target note indices = []
    #     //find the third
    #     for i, note in eumerate(prev.notes):
    #         if note == prev.chord.third:
    #             append i to target note indices
    #     foreach i in target note indices:
    #         prev.melodic_intervals[i].chromatic.direction < 0:
    #             Mark "In the Deceptive Progression (V to VI in minor keys), the 3rd of V must resolve up" error (voice #)
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
    # ***pass in prev,curr, next, and nextnext chords into this function***
    # if inversion == 2 and not 7th-chord:
    #     if not (cadential 6/4)
    #     and not (passing in bass)
    #     and not (pedal point):
    #         Mark "6/4 Chords can only be used in four cases: cadential 6/4, passing in bass, arpeggio staying on same chord, pedal point" error (whole chord)

    # cadential 6/4:
    #     return ( (next.numeral == V or next.numeral == V7) and nextnext.numeral == I)

    # passing in bass:
    #     return (areStepwise(prev.notes[3], curr.notes[3]) and areStepwise(next.notes[3], curr.notes[3]) and (prev.harmonic_interval[3].chromatic_direction * curr.harmonic_interval[3].chromatic_direction > 0)

    # pedal point:
    #     return (prev.notes[3] == curr.notes[3] == next.notes[3])

    # areStepwise(noteA, noteB):
    #     // there seriously must be a better way...
    #     return (int(noteA.name[0]) == int(noteB.name[0]) + 1) 
    #             or (int(noteA.name[0]) == int(noteB.name[0]) - 1)
    #             or (int(noteA.name[0]) == int(noteB.name[0]) + 6) 
    #             or (int(noteA.name[0]) == int(noteB.name[0]) - 6) 
    # """
    return errors