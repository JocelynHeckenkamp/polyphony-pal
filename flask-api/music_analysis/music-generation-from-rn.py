from music21 import *

# user input
key = key.Key("C")
#roman_numerals = ["vi", "ii", "V6", "iii6", "IV6", "I", "V", "V", "I", "IV6", "I6", "ii743", "ii65", "V", "I"]
roman_numerals = ["vi", "ii", "V6", "iii6", "IV6", "I", "V", "V"]

bassline = []

if __name__ == '__main__':
    print(key)

    # write bassline
    for rn in roman_numerals:
        c = roman.RomanNumeral(rn, key).pitches
        ch = chord.Chord(c)
        bassline.append(ch.root())

    print(bassline)

    # chords
    for i in range(len(roman_numerals)):
        continue
