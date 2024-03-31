from music21 import *
from . import music_xml_parser as mxp
from . import music21_method_extensions
from . import rules14to26 as r1426
from . import rules1to13 as r113
import re

music21_method_extensions.extend()


# given list of possible combos and score wrapper, try every chord
def score_bfs(sw: mxp.ScoreWrapper, chordCombos: list[list[list[note.Note]]]):
    goodChordLists = [[]]
    for combosPerChord in chordCombos:
        newGoodChordLists = []
        for combo in combosPerChord:
            for goodChordList in goodChordLists:
                currChordList = goodChordList+[combo]
                if isValid(sw, currChordList):
                    newGoodChordLists.append(currChordList)
                    if len(currChordList) == 7:
                        print(currChordList)
        goodChordLists = newGoodChordLists
    return goodChordLists


# given list of possible combos and score wrapper, try every chord
def score_dfs(sw: mxp.ScoreWrapper, lists: list[list[list[note.Note]]], index=0, prefix=[]):
    if index == len(lists):
        return [prefix]
    
    combinations = []
    for item in lists[index]:
        new_prefix = prefix + [item]
        # Add a condition here to check if new_prefix meets your criteria
        if isValid(sw, new_prefix):
            combinations.extend(score_dfs(sw, lists, index + 1, new_prefix))
            if len(new_prefix) == 7:
                print(new_prefix)
    
    return combinations


# checks if sw has errors
def isValid(sw: mxp.ScoreWrapper, chordList: list[list[note.Note]]):
    sw = addChords(sw, chordList)
    all_errors = []

    # single chord rules
    if len(sw.chord_wrappers) > 0:
        if len(r113.rule1(sw.chord_wrappers[-1])) != 0: return False  # curr, range
        if len(r113.rule2(sw.chord_wrappers[-1])) != 0: return False  # curr, spacing
        if len(r113.rule3(sw.chord_wrappers[-1])) != 0: return False  # curr, voice crossing
        # if len(r113.rule10(sw.chord_wrappers[-1])) != 0: return False  # curr, non-chords
        if len(r1426.rule14(sw.chord_wrappers[-1], sw)) != 0: return False  # Curr
        if len(r1426.rule15(sw.chord_wrappers[-1], sw)) != 0: return False  # Curr
        if len(r1426.rule16(sw.chord_wrappers[-1], sw)) != 0: return False  # Curr
        if len(r1426.rule18(sw.chord_wrappers[-1], sw)) != 0: return False  # Curr
        if len(r1426.rule19(sw.chord_wrappers[-1], sw)) != 0: return False  # Curr
        if len(r1426.rule20(sw.chord_wrappers[-1], sw)) != 0: return False  # Curr
        if len(r1426.rule22(sw.chord_wrappers[-1], sw)) != 0: return False  # Curr
        if len(r1426.rule23(sw.chord_wrappers[-1], sw)) != 0: return False  # Curr

    # two chord rules
    if len(sw.chord_wrappers) > 1:
        if len(r113.rule4(sw.chord_wrappers[-2])) != 0: return False  # curr, next, voice overlapping
        if len(r113.rule5(sw.chord_wrappers[-2])) != 0: return False  # curr, next, large melodic leaps
        if len(r113.rule9(sw.chord_wrappers[-2])) != 0: return False  # curr, next, resolving the seventh of a chord
        if len(r113.rule11(sw.chord_wrappers[-2])) != 0: return False  # curr, next, parallel octaves
        if len(r113.rule12(sw.chord_wrappers[-2])) != 0: return False  # curr, next, parallel fifths
        if len(r113.rule13(sw.chord_wrappers[-2])) != 0: return False  # curr, next, hidden fifths and octaves
        if len(r1426.rule17(sw.chord_wrappers[-2], sw)) != 0: return False  # Curr, Next
        if len(r1426.rule21(sw.chord_wrappers[-2], sw)) != 0: return False  # Curr, Next
        if len(r1426.rule24(sw.chord_wrappers[-2], sw)) != 0: return False  # Curr, Next
        if len(r1426.rule26(sw.chord_wrappers[-2], sw)) != 0: return False  # Prev, Curr, Next

    # three chord rules
    if len(sw.chord_wrappers) > 2:
        if len(r113.rule6(sw.chord_wrappers[-3])) != 0: return False  # curr, next, nextnext, double melodic leaps
        if len(r113.rule7(sw.chord_wrappers[-3])) != 0: return False  # curr, next, nextnext, resolving leaps
        if len(r113.rule8(sw.chord_wrappers[-3])) != 0: return False  # curr, next, nextnext, resolving diminished movement
    
    return True


# format score wrappers given score and chordlist
def addChords(sw: mxp.ScoreWrapper, chordList: list[list[note.Note]]):
    sw.chord_wrappers = [mxp.ChordWrapper(*chord) for chord in chordList]
    sw.format_chord_wrappers(sorted=False)
    return sw


# gets every combination given list of lists
def all_combinations(lists):
    if not lists:
        return [[]]
    
    result = [[]]
    for lst in lists:
        new_result = []
        for item in lst:
            for res in result:
                if len(res) == 0 or res[-1].geq(item): # prevent voice crossings
                    new_result.append(res + [item])
        result = new_result
    
    return result


# filters combinations by 
def filter_combinations_by_roman(chordCombos, rnStr, key):
    def remove_numbers(input_string):
        return re.sub(r'\d+', '', input_string)
    def filter_func(c: list, rn: str):
        return remove_numbers(roman.romanNumeralFromChord(chord.Chord(c), key).romanNumeral) == remove_numbers(rn)
    chordCombosFiltered = []
    for i, chordCombo in enumerate(chordCombos):
        chordCombosFiltered.append([combo for combo in chordCombo if filter_func(combo, rnStr[i])])
    return chordCombosFiltered


# gets all notes within vocal range fron chord tones
def getPossibleNotes(chordPitches: list, bassline: list):
    ranges = [
        (note.Note('C4'), note.Note('G5'), 4, 5),  # soprano
        (note.Note('G3'), note.Note('C5'), 3, 5),  # alto
        (note.Note('C3'), note.Note('G4'), 3, 4),  # tenor
        (note.Note('E2'), note.Note('C4'), 2, 4)  # bass
    ]
    possibleNotes = []
    for i, chord in enumerate(chordPitches):
        possibleNotesPerChord = []
        for voice in range(4):
            possibleNotesPerVoice = []
            for octave in range(ranges[voice][2], ranges[voice][3]+1, 1):
                if voice == 3:
                    currNote = note.Note(bassline[i].name+str(octave))
                    if currNote.leq(ranges[voice][1]) and currNote.geq(ranges[voice][0]):
                        possibleNotesPerVoice.append(currNote)
                else:
                    for pitch in chord:
                        currNote = note.Note(pitch+str(octave))
                        if currNote.leq(ranges[voice][1]) and currNote.geq(ranges[voice][0]):
                            possibleNotesPerVoice.append(currNote) 
            possibleNotesPerChord.append(possibleNotesPerVoice)
        possibleNotes.append(possibleNotesPerChord)
    return(possibleNotes)


# gets all notes in vocal range
def getVoiceRanges():
    ranges = [
        ('C4', 'C#4', 
        'D-4', 'D4', 'D#4', 
        'E-4', 'E4', 'E#4', 
        'F-4', 'F4', 'F#4', 
        'G-4', 'G4', 'G#4', 
        'A-4', 'A4', 'A#4', 
        'B-4', 'B4', 'B#4',
        'C-5', 'C5', 'C#5',
        'D-5', 'D5', 'D#5', 
        'E-5', 'E5', 'E#5', 
        'F-5', 'F5', 'F#5', 
        'G-5', 'G5'),  # soprano

        ('G3', 'G#3', 
        'A-3', 'A3', 'A#3', 
        'B-3', 'B3', 'B#3',
        'C-4', 'C4', 'C#4', 
        'D-4', 'D4', 'D#4', 
        'E-4', 'E4', 'E#4', 
        'F-4', 'F4', 'F#4', 
        'G-4', 'G4', 'G#4', 
        'A-4', 'A4', 'A#4', 
        'B-4', 'B4', 'B#4',
        'C-5', 'C5'),  # alto

        ('C3', 'C#3', 
        'D-3', 'D3', 'D#3', 
        'E-3', 'E3', 'E#3', 
        'F-3', 'F3', 'F#3', 
        'G-3', 'G3', 'G#3', 
        'A-3', 'A3', 'A#3', 
        'B-3', 'B3', 'B#3',
        'C-4', 'C4', 'C#4', 
        'D-4', 'D4', 'D#4', 
        'E-4', 'E4', 'E#4', 
        'F-4', 'F4', 'F#4', 
        'G-4', 'G4'),  # tenor

        ('E2', 'E#2', 
        'F-2', 'F2', 'F#2', 
        'G-2', 'G2', 'G#2', 
        'A-2', 'A2', 'A#2', 
        'B-2', 'B2', 'B#2',
        'C-3', 'C3', 'C#3',
        'D-3', 'D3', 'D#3', 
        'E-3', 'E3', 'E#3', 
        'F-3', 'F3', 'F#3', 
        'G-3', 'G3', 'G#3', 
        'A-3', 'A3', 'A#3', 
        'B-3', 'B3', 'B#3',
        'C-4', 'C4')  # bass
    ]

    # make notes out of the pitch names
    noteRanges = []
    for voice in ranges:
        noteRanges.append(tuple(map(lambda x: note.Note(x), voice)))
    return noteRanges


# gets bassline and chord tones from roman numerals and key
def analyzeRN(rnStr: str, keyStr: str):
    # write bassline
    bassline = []
    chordPitches = []
    for rn in rnStr:
        c = roman.RomanNumeral(rn, key.Key(keyStr)).pitches
        ch = chord.Chord(c)
        chordPitches.append( list(map((lambda x : x.name), ch.notes)) )
        bassline.append(ch[0])
    return bassline, chordPitches


