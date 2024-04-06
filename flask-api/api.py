
from flask import Flask, request, jsonify, render_template
import music_analysis.rules1to13 as r113
import music_analysis.rules14to26 as r1426
import music_analysis.music_xml_parser as mxp
import music_analysis.music_generation_encapsulated as gen
from music_analysis.error import Error as e
app = Flask(__name__)




#Currently Prints the File sent to this route
@app.route('/upload', methods=['PUT'])
def music_upload():
    musicXML = request.get_data(False, True, False)
    #run script then return
    content = "{} {}".format(musicXML, errors(musicXML))
    return content

@app.route('/musicGeneration', methods=['POST'])
def music_generation():
    romanNumerals = request.get_data(False, True, False)
    #run script then return
    xml = gen.musicGenerationFromRomanToStr(romanNumerals, "C", verbose=True)
    return xml


def errors(musicXML):
    errors = []
    sw = mxp.getScoreWrapper(musicXML)
    curr = sw.chord_wrappers[0]
    while(curr is not None):
        errors.extend(r113.check_rules_1_to_13(curr, sw))
        errors.extend(r1426.check_rules_14_to_26(curr, sw))
        curr = curr.next
    return [error.__dict__ for error in errors]


if __name__ == '__main__':
    app.run(debug=True)

