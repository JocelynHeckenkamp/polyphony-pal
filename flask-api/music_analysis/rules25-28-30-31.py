from . import error as e
import music21
from . import music_xml_parser as mxp
from . import music21_method_extensions
WHOLE_CHORD = [True, True, True, True]
voice_names = ["Soprano", "Alto", "Tenor", "Bass"]
voice_names_lower = ["soprano", "alto", "tenor", "bass"]

def check_rules_25_28_30_31(chord: mxp.ChordWrapper, score: mxp.ScoreWrapper):
    music21_method_extensions.extend()

    all_errors = []

    return all_errors