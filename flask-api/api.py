
from flask import Flask, request, jsonify, json
import logging
import os

#database/API
from database.ext import db  # Updated to reflect new path
from database.config import Config  # Updated if config.py was moved; otherwise, keep as 'from config import Config'
from database.query import roman_score_query, romanid_XML_query, add_romanScore


#rules imports
import music_analysis.rules1to13 as r113
import music_analysis.rules14to26 as r1426
import music_analysis.rule27 as r27
import music_analysis.rules25_28_31 as rules252831
import music_analysis.music_xml_parser as mxp
import music_generation.counterpoint_generation as cpg
from music_analysis.error import Error as e

#database model
from database.models import *

app = Flask(__name__)
app.config.from_object(Config)
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
db.init_app(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# #database initialized before any requests
with app.app_context():
    db.create_all()

def calcErrors(musicXML):
    errorList = []
    doubling_errors = []
    sw = mxp.getScoreWrapper(musicXML)
    errorList.extend(r27.check_rule_27(sw))
    
    curr = sw.chord_wrappers[0]
    while(curr is not None):
        errorList.extend(r113.check_rules_1_to_13(curr, sw))
        errorList.extend(rules252831.check_rules_25_28to31(curr, sw))
        doubling_errors.extend(r1426.check_rules_14_to_26(curr, sw))
        curr = curr.next
    return [error.__dict__ for error in errorList], [error.__dict__ for error in doubling_errors]

#Currently Prints the File sent to this route
@app.route('/upload', methods=['PUT'])
def music_upload():
    musicXML = request.get_data(False, True, False)
    #run script then return
    errors, doubling_errors = calcErrors(musicXML)
    return jsonify({'errors': errors, 'suggestions': doubling_errors}), 200


@app.route('/counterpoint', methods=['PUT'])
def counterpoint():
    musicXML = request.get_data(False, True, False)
    counterpoints = cpg.generate_counterpoint(musicXML, 1)
    counterpoints = json.dumps(counterpoints)
    return counterpoints



@app.route('/musicGeneration', methods=['POST'])
def music_generation():
    req = request.get_json()
    req = req['values']
    romanNumerals = req[1]
    key = req[0]
    # xml = gen.musicGenerationFromRomanToStr(romanNumerals, key, verbose=True)
    # return xml

    romanScore = RomanScore.query.filter_by(roman=romanNumerals, key=key).first()
    if (romanScore):
        return jsonify(romanScore.serialize()), 201

    new_romanScore = RomanScore(
        roman=romanNumerals,
        key=key,
        finished=False,
    )

    db.session.add(new_romanScore)
    db.session.commit()

    id = new_romanScore.id
    app.logger.debug(f"Debug message: Request received! {id}")
    
    # Path to the Python script you want to run
    script_path = './musicGenerationRunner.py'

    # Command to run the script in the background using os.system
    command = f'python {script_path} {romanNumerals} {key} {id} &'

    # Execute the command to run the script in the background
    os.system(command)

    # # roman_score_finish(id)
    # app.logger.debug(f"Combos: {combos}")
    return jsonify(new_romanScore.serialize()), 201


@app.route('/RomanScore/<int:id>', methods=['PUT'])
def update_RomanScore(id: int):
    romanScore = RomanScore.query.get(id)
    if not romanScore:
        return jsonify({'message': 'romanScore not found'}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(romanScore, key):
            setattr(romanScore, key, value)

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200


@app.route('/XML', methods=['POST'])
def add_XML():
    req = request.get_json()
    roman_id = req['roman_id']
    xml = req['xml']

    new_XML = XML(
        xml=xml,
        roman_id=roman_id,
    )

    db.session.add(new_XML)
    db.session.commit()

    return jsonify(new_XML.serialize()), 201


@app.route('/RomanScore/<int:id>/XML', methods=['GET'])
def get_XML(id: int):
    max_xmls = int(request.args.get('max_xmls', 50))
    score = RomanScore.query.get(id)
    xmls = [{'xml':x.xml, 'id':x.id} for x in score.xmls[:min(len(score.xmls), max_xmls)]]
    return jsonify({'xmls': xmls, 'finished': score.finished}), 201 


if __name__ == '__main__':
    app.run(debug=True)

