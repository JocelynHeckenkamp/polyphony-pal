
from flask import Flask, request, jsonify, render_template

#database/API
from database.ext import db  # Updated to reflect new path
from database.config import Config  # Updated if config.py was moved; otherwise, keep as 'from config import Config'


#rules imports
import music_analysis.rules1to13 as r113
import music_analysis.rules14to26 as r1426
import music_analysis.music_xml_parser as mxp
import music_analysis.music_generation_encapsulated as gen
from music_analysis.error import Error as e

#database model
from database.models import *

app = Flask(__name__)
app.config.from_object(Config)
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
db.init_app(app)

# #database initialized before any requests
# app.register_blueprint(api_bp)
with app.app_context():
    db.create_all()

#Currently Prints the File sent to this route
@app.route('/upload', methods=['PUT'])
def music_upload():
    musicXML = request.get_data(False, True, False)
    #run script then return
    content = "{} {}".format(musicXML, errors(musicXML))
    return content

def errors(musicXML):
    errors = []
    sw = mxp.getScoreWrapper(musicXML)
    curr = sw.chord_wrappers[0]
    while(curr is not None):
        errors.extend(r113.check_rules_1_to_13(curr, sw))
        errors.extend(r1426.check_rules_14_to_26(curr, sw))
        curr = curr.next
    return [error.__dict__ for error in errors]

@app.route('/musicGeneration', methods=['POST'])
def music_generation():
    req = request.get_json()
    req = req['values']
    romanNumerals = req[1].split(",")
    key = req[0]
    xml = gen.musicGenerationFromRomanToStr(romanNumerals, key, verbose=True)
    return xml
    # new_romanScore = RomanScore(
    #         roman=req[1],
    #         key=key,
    #         finished=False,
    #         most_recent_XML=None,
    #     )

    # db.session.add(new_romanScore)
    # db.session.commit()

    # return jsonify(new_romanScore.serialize()), 201

if __name__ == '__main__':
    app.run(debug=True)

