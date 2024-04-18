from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import func, desc, or_, String, cast
from sqlalchemy import func, or_, text
from flask import jsonify
from .ext import db
from .models import *

def roman_score_query(roman: str, key: str):
    query = text("""
        SELECT id FROM "RomanScore"
        WHERE roman = :roman_value AND key = :key_value
    """)

    results = []
    with db.session.begin():
        # Execute the SQL query with user inputs as parameters
        query_results = db.session.execute(
            query, 
            {'roman_value': roman, 'key_value': key}
        )
        
        # Store the results in a list of dictionaries
        results = [row[0] for row in query_results]

    # Return the results as list
    return results



def romanid_XML_query(roman_id: int):
    query = text("""
        SELECT xml FROM "XML"
        WHERE roman_id = :romanid
    """)

    results = []
    with db.session.begin():
        # Execute the SQL query with user inputs as parameters
        query_results = db.session.execute(
            query, 
            {'romanid': roman_id}
        )
        
        # Store the results in a list of dictionaries
        results = [row[0] for row in query_results]


    # Return the results as list
    return results


def add_romanScore(romanNumerals: str, key: str):
    new_romanScore = RomanScore(
        roman=romanNumerals,
        key=key,
        finished=False,
        most_recent_XML=None,
    )

    db.session.add(new_romanScore)
    db.session.commit()

    # idd = new_romanScore.serialize()["id"]
    id = roman_score_query(romanNumerals, key)[0]

    return id, jsonify(new_romanScore.serialize()), 201


# def add_XML(roman_id: int, xml: str):
#     new_XML = XML(
#         xml=xml,
#         roman_id=roman_id,
#     )

#     db.session.add(new_XML)
#     db.session.commit()

#     return jsonify(new_XML.serialize()), 201