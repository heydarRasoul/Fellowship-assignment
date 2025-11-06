from flask import request, jsonify

from db import db
from models.abilities import Abilities, ability_schema, abilities_schema
from util.reflection import populate_object

def add_ability():
    post_data = request.form if request.form else request.get_json()

    new_ability= Abilities.new_ability_obj()
    populate_object(new_ability, post_data)

    try:
        db.session.add(new_ability)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"messsage":"unable to create ability"}),400
    
    return jsonify({"message":"ability created", "result": ability_schema.dump(new_ability)}),201




def update_ability_by_id(ability_id):
    post_data = request.form if request.form else request.get_json()

    query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

    if query:
        populate_object(query, post_data)

        db.session.commit()
   
        return jsonify({"message": "ability found", "results": ability_schema.dump(query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400



def delete_ability_by_id(ability_id):
    query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

    if query:
        db.session.delete(query)
        db.session.commit()

        return jsonify({"message":"ability deleted"}),200
    
    return jsonify({"message":"unable to delete ability"}), 400
        
    