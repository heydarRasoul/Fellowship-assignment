from flask import jsonify, request

from db import db
from models.quests import Quests, quest_schema, quests_schema
# from models.abilities import Categories
from util.reflection import populate_object


# CREATE
def create_quest():
    post_data = request.form if request.form else request.get_json()

    new_quest = Quests.new_quest_obj()
    populate_object(new_quest, post_data)

    try:
        db.session.add(new_quest)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "quest created", "result": quest_schema.dump(new_quest)}), 201


def get_quest_difficulty_level():
    difficulty_level_query = db.session.query(Quests).filter(Quests.difficulty_level).all()

    if not difficulty_level_query:
        return jsonify({"message":"no quest found"}),400
    else:
        return jsonify({"message":"quest found", "results":quest_schema.dump(difficulty_level_query)}),200
    

def get_quest_by_id(quest_id):
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not quest_query:
        return jsonify ({"message":"no result found for provided id"}),400
    else:
        return jsonify ({"message":"quest found", "result": quest_schema.dump(quest_query)}), 200


# UPDATE

def update_quest_by_id(quest_id):
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()
    post_data = request.form if request.form else request.get_json()

    if quest_query:
        populate_object(quest_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "quest found", "results": quest_schema.dump(quest_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400


def mark_quest_complete(quest_id):
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not quest_query:
        return jsonify({"message": "quest not found"}), 400
    
    quest_query.is_completed = True
    
    db.session.commit()
   
    return jsonify({"message": "quest found", "results": quest_schema.dump(quest_query)}), 200
    
    


# DELETE


def delete_quest_by_id(quest_id):
    query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if query:
        db.session.delete(query)
        db.session.commit()

        return jsonify({"message":"quest deleted"}),200
    
    return jsonify({"message":"unable to delete quest"}), 400
        
    