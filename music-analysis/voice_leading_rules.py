from music21 import *
import music_xml_parser

filename = "../music-xml-examples/voice-leading-7.musicxml"

class Error:
    title = None
    location = set()
    description = None
    suggestion = None
    def __init__(self, title, location, description, suggestion):
        self.title = title
        self.location = location
        self.description = description
        self.suggestion = suggestion

    def __str__(self):
        return f"{self.title({self.location})}"

#def getErrors():
if __name__ == '__main__':
    chords, locations, sc = music_xml_parser.parse_XML(filename)

    # key signature

