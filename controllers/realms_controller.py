
from flask import request, jsonify

from db import db
from models.realms import Realms, realms_schema, realm_schema
from util.reflection import populate_object

def add_realm():
    post_data = request.form if request.form else request.get_json()

    new_realm = Realms.new_realm_obj()
    populate_object(new_realm, post_data)

    try:
        db.session.add(new_realm)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "realm created", "result": realm_schema.dump(new_realm)}), 201


def get_realm_by_id(realm_id):
    realm_query = db.session.query(Realms).filter(Realms.realm_id == realm_id ).first()

    if not realm_query:
        return jsonify({"message": "no realm with provided id founded."})
    else:
        return jsonify({"message": "realm found", "result": realm_schema.dump(realm_query)}),200
    

def update_realm_by_id(realm_id):
    realm_query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()
    post_data = request.form if request.form else request.get_json()

    if realm_query:
        populate_object(realm_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "realm found", "results": realm_schema.dump(realm_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400


def delete_realm_by_id(realm_id):
    realm_query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

    if realm_query:
        db.session.delete(realm_query)
        db.session.commit()

        return jsonify({"message":"realm deleted"}),200
    
    return jsonify({"message":"unable to delete realm"}), 400
        
    