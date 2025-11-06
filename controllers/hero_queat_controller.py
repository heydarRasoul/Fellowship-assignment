from flask import jsonify, request
from datetime import datetime

from db import db
from models.hero_quest import HeroQuests, heroQuests_schema, heroQuest_schema
from models.heros import Heros
from models.quests import Quests
from util.reflection import populate_object





def add_hero_to_quest():
    post_data = request.form if request.form else request.get_json()
    hero_id= post_data.get("hero_id")
    quest_id= post_data.get("quest_id")

    hero_query = db.session.query(Heros).filter(Heros.hero_id==hero_id).first()
    quest_query = db.session.query(Quests).filter(Quests.quest_id==quest_id).first()

    if not hero_query:
        return jsonify({"message": "hero not found"}), 404

    if not quest_query:
        return jsonify({"message":"quest not found"}),404
    
    existing = db.session.query(HeroQuests).filter_by(hero_id=hero_id, quest_id=quest_id).first()
    if existing:
        return jsonify({"message": "Hero already assigned to this quest"}), 400

    new_hero_quests = HeroQuests.new_hero_quest_obj()
    populate_object(new_hero_quests, post_data)

    # hero_query.quests.append(quest_query)


    db.session.commit()
    return jsonify({"message":"hero added to quest", "result": heroQuest_schema.dump(new_hero_quests)}),200

