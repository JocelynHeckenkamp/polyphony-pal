import music_analysis.music_xml_parser as mxp
# import music_analysis.error as e
# import music_analysis.rule27 as r27
# import music_analysis.rules1to13 as r113
# import music_analysis.rules14to26 as r1426
import music_analysis.music_generation_from_rn as gen
import music21

if __name__ == '__main__':
    # user input
    keyStr = "C"
    #roman_numerals = ["vi", "ii", "V6", "iii6", "IV6", "I", "V", "V", "I", "IV6", "I6", "ii743", "ii65", "V", "I"]
    roman_numerals = ["vi", "ii", "V6", "iii6", "IV6", "I", "V", "V"]
    sw = mxp.ScoreWrapper().initKey(keyStr)
    # write bassline
    bassline, chordPitches = gen.analyzeRN(roman_numerals, keyStr)
    print(chordPitches)
    print(list(map((lambda x : x.name), bassline)))

    print(gen.getVoiceRanges())