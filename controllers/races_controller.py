from flask import jsonify, request

from db import db
from models.races import Races, race_schema, races_schema
# from models.abilities import Abilities
from util.reflection import populate_object


# CREATE
def create_race():
    post_data = request.form if request.form else request.get_json()

    new_race = Races.new_race_obj()
    populate_object(new_race, post_data)

    try:
        db.session.add(new_race)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "race created", "result": race_schema.dump(new_race)}), 201



# READ
def get_all_races():
    races_query = db.session.query(Races).all()

    if not races_query:
        return jsonify({"message":"no race found"}),404
    
    else:
        return jsonify({"message":"races found", "results": races_schema.dump(races_query)}), 200


def get_race_by_id(race_id):
    race_query = db.session.query(Races).filter(Races.race_id == race_id).first()

    if not race_query:
        return jsonify ({"message":"no result found for provided id"}),400
    else:
        return jsonify ({"message":"race found", "result": race_schema.dump(race_query)}), 200


# UPDATE

def update_race_by_id(race_id):
    race_query = db.session.query(Races).filter(Races.race_id == race_id).first()
    post_data = request.form if request.form else request.get_json()

    if race_query:
        populate_object(race_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "race found", "results": race_schema.dump(race_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400

# DELETE


def delete_race_by_id(race_id):
    query = db.session.query(Races).filter(Races.race_id == race_id).first()

    if query:
        db.session.delete(query)
        db.session.commit()

        return jsonify({"message":"race deleted"}),200
    
    return jsonify({"message":"unable to delete race"}), 400
        
    