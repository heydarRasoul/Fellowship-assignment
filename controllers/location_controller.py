from flask import request, jsonify

from db import db
from models.location import Locations, location_schema, locations_schema
from util.reflection import populate_object



def add_location():
    post_data = request.form if request.form else request.get_json()

    location = Locations.new_location_obj()
    populate_object(location, post_data)

    try:
        db.session.add(location)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"messsage":"unable to create location"}),400
    
    return jsonify({"message":"location created", "result": location_schema.dump(location)}),201


def get_location_by_id(location_id):
    query = db.session.query(Locations).filter(Locations.location_id == location_id ).first()

    if not query:
        return jsonify({"message": "no location with provided id founded."})
    else:
        return jsonify({"message": "location found", "result": location_schema.dump(query)}),200
    

def update_location_by_id(location_id):
    query = db.session.query(Locations).filter(Locations.location_id == location_id).first()
    post_data = request.form if request.form else request.get_json()

    if query:
        populate_object(query, post_data)

        db.session.commit()
   
        return jsonify({"message": "location found", "results": location_schema.dump(query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400


def delete_location_by_id(location_id):
    query = db.session.query(Locations).filter(Locations.location_id == location_id).first()

    if query:
        db.session.delete(query)
        db.session.commit()

        return jsonify({"message":"location deleted"}),200
    
    return jsonify({"message":"unable to delete location"}), 400
        
    