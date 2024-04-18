from . import music_xml_parser as mxp
from . import music_generation_from_rn as gen
import requests
from music21 import *

import sys

URL = "http://localhost:5000"

def musicGenerationFromRomanToFiles(roman_numerals: list[str], keyStr:str, limit = 10, verbose = False, verboseLong = False):
    # write bassline
    bassline, chordPitches = gen.analyzeRN(roman_numerals, keyStr)
    if verbose:
        print("Chord Tones:", chordPitches, "\n")
        print("Bassline:", list(map((lambda x : x.name), bassline)), "\n")

    # get possible notes (with octave) per voice
    possibleNotes = gen.getPossibleNotes(chordPitches, bassline)

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


def musicGenerationFromRomanToStr(roman_numerals: list[str], keyStr:str, id: int, limit = 10, verbose = False, verboseLong = False):
    # write bassline
    bassline, chordPitches = gen.analyzeRN(roman_numerals, keyStr)
    if verbose:
        print("Chord Tones:", chordPitches, "\n")
        print("Bassline:", list(map((lambda x : x.name), bassline)), "\n")

    # get possible notes (with octave) per voice
    possibleNotes = gen.getPossibleNotes(chordPitches, bassline)

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
    combos = gen.score_dfs_iterative(roman_numerals, sw, chordCombos, id, limit=limit, verbose=verbose, verboseLong=verboseLong)

    # add xml to XML table
    data = {
        'finished': True,
    }
    requests.put(f"{URL}/RomanScore/{id}", json=data)

    if len(combos) == 0: 
        print("Could not find any valid harmonizations of the current chord progression.") 
        return None
    else: 
        return combos


if __name__ == '__main__':
    script_name = sys.argv[0]  
    romanNumerals = sys.argv[1]       
    key_ = sys.argv[2]       
    id = sys.argv[3]
    musicGenerationFromRomanToStr(romanNumerals.split(","), key_, id, limit = 10)




