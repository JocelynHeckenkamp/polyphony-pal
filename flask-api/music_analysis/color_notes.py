import xml.etree.ElementTree as et
from music21 import *
from bs4 import BeautifulSoup
import xml

fn = "./voice-leading-1.musicxml"
# fn = "./parallel_5ths.musicxml"

def color_notes(musicxml, measure, offset, voices):

    soup = BeautifulSoup(musicxml, "xml")

    npm = int(soup.find("time").find("beats").text)
    measures = soup.find_all("measure")
    mm = measures[measure]
    for v in range(len(voices)):
        if voices[v]:
            i = v * npm + int(offset)
            note = mm.find_all("note")[i]
            note["color"] = "#CC0000"

            # notehead = soup.new_tag("notehead", color="#CC0000")
            # # notehead["color"] = "#CC0000"
            # notehead.string = "normal"
            # note.append(notehead)
            # note.staff.insert_before(notehead)
            # print(note.find("pitch").find("step"))

    # new_mxml = soup.prettify()
    new_mxml = soup

    return new_mxml

if __name__ == '__main__':

    mxml = None
    with open(fn, 'r') as f:
        mxml = f.read()
    new_mxml = color_notes(mxml, 0, 0.0, [True, True, True, True])

    print(new_mxml)

    # s = converter.parse(new_mxml)
    # s.show()