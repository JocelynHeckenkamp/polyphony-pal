from . import error as e
from . import music_xml_parser as mxp
WHOLE_CHORD = [True, True, True, True]
def check_rule_27(score: mxp.ScoreWrapper):
        errors = []

        # rule 27: key signatures
        if (score.key != score.key_signature):
            suggestion = f"Suggested key: {score.key}"

            accidentals = score.key.sharps
            if accidentals > 1: # surprised there is nothing in music21 for this
                suggestion += f" ({accidentals} shaprs)"
            elif accidentals == 0:
                suggestion += f" (no accidentals)"
            else:
                suggestion += f" ({abs(accidentals)} flats)"

            ErrorParams = {
                'title': 'Key Signature Error',
                'location': -1,  # unique value for key signature errors
                'description': "Your voice leading is best suited for another key signature.",
                'suggestion': suggestion,
                'voices': [False] * 4,
                'duration': -1,
            }

            errors.append(e.Error(**ErrorParams))

        return errors