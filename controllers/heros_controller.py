from flask import jsonify, request

from db import db
from models.heros import Heros, hero_schema, heros_schema
from models.hero_quest import HeroQuests
from util.reflection import populate_object
from models.quests import Quests


# CREATE
def create_hero():
    post_data = request.form if request.form else request.get_json()

    new_hero = Heros.new_hero_obj()
    populate_object(new_hero, post_data)

    try:
        db.session.add(new_hero)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "hero created", "result": hero_schema.dump(new_hero)}), 201

# def add_hero_to_quest():
#     post_data = request.form if request.form else request.get_json()
#     hero_id= post_data.get("hero_id")
#     quest_id= post_data.get("quest_id")

#     hero_query = db.session.query(Heros).filter(Heros.hero_id==hero_id).first()
#     quest_query = db.session.query(Quests).filter(Quests.quest_id==quest_id).first()

#     if not hero_query:
#         return jsonify({"message": "hero not found"}), 404

#     if not quest_query:
#         return jsonify({"message":"quest not found"}),404
    
#     existing = db.session.query(HeroQuests).filter_by(hero_id=hero_id, quest_id=quest_id).first()
#     if existing:
#         return jsonify({"message": "Hero already assigned to this quest"}), 400

    
#     hero_query.quests.append(quest_query)


#     db.session.commit()
#     return jsonify({"message":"hero added to quest", "result": hero_schema.dump(hero_query)}),200


def get_all_heros():
    heros_query = db.session.query(Heros).all()

    if not heros_query:
        return jsonify({"message":"no products found"}),404
    
    else:
        return jsonify({"message":"heros found", "results": heros_schema.dump(heros_query)}), 200


def get_alive_heros():
    alive_heros_query = db.session.query(Heros).filter(Heros.is_alive).all()

    if not alive_heros_query:
        return jsonify({"message":"no alive hero found"}),400
    else:
        return jsonify({"message":"heros found", "results":heros_schema.dump(alive_heros_query)}),200


def get_hero_by_id(hero_id):
    hero_query = db.session.query(Heros).filter(Heros.hero_id == hero_id).first()

    if not hero_query:
        return jsonify ({"message":"no result found for provided id"}),400
    else:
        return jsonify ({"message":"hero found", "result": hero_schema.dump(hero_query)}), 200


def get_quest_by_hero(hero_id):
    query = db.session.query(Heros).filter(Heros.hero_id == hero_id).first()

    if not query:
        return jsonify ({"message":"no result found"}),400
    
    quests_list = []
    for hero_quest in query.heroQuests:
        quests_list.append(hero_quest.quests)

    if not quests_list:
        return jsonify({"message":"no quest found for this hero"})
    
    
    return jsonify ({"message":"quests found", "result": hero_schema.dump(quests_list)}), 200

# UPDATE

def update_hero_by_id(hero_id):
    hero_query = db.session.query(Heros).filter(Heros.hero_id == hero_id).first()
    post_data = request.form if request.form else request.get_json()

    if hero_query:
        populate_object(hero_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "hero found", "results": hero_schema.dump(hero_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400

# DELETE


def delete_hero_by_id(hero_id):
    query = db.session.query(Heros).filter(Heros.hero_id == hero_id).first()

    if query:
        db.session.delete(query)
        db.session.commit()

        return jsonify({"message":"hero deleted"}),200
    
    return jsonify({"message":"unable to delete hero"}), 400
        
    