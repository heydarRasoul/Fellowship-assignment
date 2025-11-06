import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Races(db.Model):
    __tablename__ = "Races"

    	
    race_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    race_name = db.Column(db.String(), nullable=False, unique=True)
    homeland = db.Column(db.String())
    lifespan = db.Column(db.Integer())


    heros = db.relationship("Heros", foreign_keys="[Heros.race_id]", back_populates='races', cascade="all")


    def __init__(self, race_name, homeland, lifespan):
        self.race_name = race_name
        self.homeland = homeland
        self.lifespan = lifespan
    

    def new_race_obj():
        return Races('', '', '')


class RacesSchema(ma.Schema):
    
    class Meta:
        fields = ['race_id', 'race_name', 'homeland', 'lifespan']

    race_id = ma.fields.UUID()
    race_name = ma.fields.String(required=True)
    homeland = ma.fields.String(allow_none=True)
    lifespan = ma.fields.Integer(allow_none=True)

   
    
race_schema = RacesSchema()
races_schema = RacesSchema(many=True)