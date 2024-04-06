import music_analysis.music_xml_parser as mxp
import music_analysis.music_generation_from_rn as gen
from music21 import *

def musicGenerationFromRomanToFiles(roman_numerals: list[str], keyStr:str, limit = 10, verbose = False, verboseLong = False):
    # write bassline
    bassline, chordPitches = gen.analyzeRN(roman_numerals, keyStr)
    if verbose:
        print("Chord Tones:", chordPitches, "\n")
        print("Bassline:", list(map((lambda x : x.name), bassline)), "\n")

    # get possible notes (with octave) per voice
    possibleNotes = gen.getPossibleNotes(chordPitches, bassline)

    # set first chord
    possibleNotes[0] = [[note.Note("B4")], [note.Note("D4")], [note.Note("G3")], [note.Note("G3")]] 
    if verbose:
        print("Possible Notes:")
        for chordPN in possibleNotes:
            print("sopreno: ", list(map((lambda x : x.nameWithOctave), chordPN[0])))
            print("alto: ", list(map((lambda x : x.nameWithOctave), chordPN[1])))
            print("tenor: ", list(map((lambda x : x.nameWithOctave), chordPN[2])))
            print("bass: ", list(map((lambda x : x.nameWithOctave), chordPN[3])), "\n")

    # get all combinations
    chordCombos = []
    total = 1
    for chordPN in possibleNotes:
        combos = gen.all_combinations(chordPN)
        total *= len(combos)
        if verbose and verboseLong:
            print(list(map((lambda x: list(map((lambda y: y.nameWithOctave), x))), combos)))
        chordCombos.append(combos)
    if verbose:
        print("total number of chord note combos:", total)

    # get all good chordlists
    sw = mxp.ScoreWrapper().initKey(keyStr)
    goodChordLists = gen.score_dfs_iterative(roman_numerals, sw, chordCombos, limit=limit, verbose=verbose, verboseLong=verboseLong)

    if len(goodChordLists) == 0: print("Could not find any valid harmonizations of the current chord progression.") 


def musicGenerationFromRomanToStr(roman_numerals: list[str], keyStr:str, limit = 1, verbose = False, verboseLong = False):
    # write bassline
    bassline, chordPitches = gen.analyzeRN(roman_numerals, keyStr)
    if verbose:
        print("Chord Tones:", chordPitches, "\n")
        print("Bassline:", list(map((lambda x : x.name), bassline)), "\n")

    # get possible notes (with octave) per voice
    possibleNotes = gen.getPossibleNotes(chordPitches, bassline)

    # set first chord
    possibleNotes[0] = [[note.Note("B4")], [note.Note("D4")], [note.Note("G3")], [note.Note("G3")]] 
    if verbose:
        print("Possible Notes:")
        for chordPN in possibleNotes:
            print("sopreno: ", list(map((lambda x : x.nameWithOctave), chordPN[0])))
            print("alto: ", list(map((lambda x : x.nameWithOctave), chordPN[1])))
            print("tenor: ", list(map((lambda x : x.nameWithOctave), chordPN[2])))
            print("bass: ", list(map((lambda x : x.nameWithOctave), chordPN[3])), "\n")

    # get all combinations
    chordCombos = []
    total = 1
    for chordPN in possibleNotes:
        combos = gen.all_combinations(chordPN)
        total *= len(combos)
        if verbose and verboseLong:
            print(list(map((lambda x: list(map((lambda y: y.nameWithOctave), x))), combos)))
        chordCombos.append(combos)
    if verbose:
        print("total number of chord note combos:", total)

    # get all good chordlists
    sw = mxp.ScoreWrapper().initKey(keyStr)
    xml = gen.score_dfs_iterative(roman_numerals, sw, chordCombos, limit=limit, verbose=verbose, verboseLong=verboseLong, strOut=True)

    if len(xml) == 0: 
        print("Could not find any valid harmonizations of the current chord progression.") 
        return None
    else: 
        return xml 


if __name__ == '__main__':
   # user input
    keyStr = "G"
    # roman_numerals = ["vi", "ii", "V6", "iii6", "IV6", "I", "V", "V", "I", "IV6", "I6", "ii743", "ii65", "V", "I"]
    # roman_numerals = ["vi", "ii", "V6", "iii6", "IV6", "I", "V"]
    # roman_numerals = ["I", "iio", "I", "vi", "I64", "V7", "I"]
    # roman_numerals = ["I6", "iii6", "vi6", "ii", "V7/V", "V6", "V"]
    roman_numerals = ["I", "V6", "vi", "V43/IV", "IV", "ii7", "V"]
    print(musicGenerationFromRomanToStr(roman_numerals, keyStr, verbose=True))


