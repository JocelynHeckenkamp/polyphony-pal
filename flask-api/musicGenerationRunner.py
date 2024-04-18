from music_analysis import music_generation_encapsulated as m
import sys

if __name__ == '__main__':
    script_name = sys.argv[0]  
    romanNumerals = sys.argv[1]       
    key_ = sys.argv[2]       
    id = sys.argv[3]
    m.musicGenerationFromRomanToStr(romanNumerals.split(","), key_, id, limit = 100000)