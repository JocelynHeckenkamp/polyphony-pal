import xml.etree.ElementTree as et
from music21 import *
from bs4 import BeautifulSoup

fn = "./voice-leading-1.musicxml"

def find_indices(soup, measure, offset, voices):

    indices = []

    npm = int(soup.find("time").find("beats").text)

    print(npm)

    notes = soup.find_all("note")
    npv = len(notes) / 4 # notes per voice


    for v in range(len(voices)):
        if voices[v]:
            i = v * npv


    return indices

def color_notes(musicxml, measure, offset, voices):

    soup = BeautifulSoup(musicxml, "xml")

    # notes = soup.find_all("note")
    # indices = find_indices(soup, measure, offset, voices)
    # print(indices)

    npm = int(soup.find("time").find("beats").text)
    measures = soup.find_all("measure")
    mm = measures[measure]
    for v in range(len(voices)):
        if voices[v]:
            i = v * npm + int(offset)
            note = mm.find_all("note")[i]
            notehead = et.SubElement(note, "notehead")
            notehead.set("color", "#CC0000")

            print(note.find("pitch").find("step"))
            print(notehead)


    new_mxml = None

    return new_mxml

if __name__ == '__main__':

    mxml = None

    with open(fn, 'r') as f:
        mxml = f.read()

    new_mxml = color_notes(mxml, 1, 2.0, [True, True, True, True])

    s = converter.parse(mxml)
    s.show()