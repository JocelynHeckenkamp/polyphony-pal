import time
from flask import Flask, request, jsonify, render_template
import music_analysis.rules1to13 as r113
import music_analysis.rules14to26 as r1426
import music_analysis.music_xml_parser as mxp
from music_analysis.error import Error as e
app = Flask(__name__)


@app.route('/time')
def get_current_time():
    return {'time': time.time()}

#Currently Prints the File sent to this route
@app.route('/upload', methods=['PUT'])
def music_upload():
    musicXML = request.get_data(False, True, False)
    #run script then return
    content = "{} {}".format(musicXML, errors(musicXML))
    return content

# @app.route('/results', methods=['GET', 'POST'])
# def music_return():
#     f = open(r'voice-leading-1.mxml', "r")
#     x = f.read()
#     return x

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

