import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .hero_quest import HeroQuests

class Heros(db.Model):
    __tablename__ = "Heros"

    hero_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    race_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Races.race_id"), nullable=False)
    hero_name = db.Column(db.String(), nullable=False, unique=True)
    age = db.Column(db.Integer())
    health_points = db.Column(db.Integer())
    is_alive = db.Column(db.Boolean(), default=True)

    abilities = db.relationship("Abilities", foreign_keys="[Abilities.hero_id]", back_populates='heros', cascade="all")
    races = db.relationship("Races", foreign_keys='[Heros.race_id]', back_populates='heros')
    heroQuests = db.relationship("HeroQuests", back_populates="heros", cascade="all")


    def __init__(self, hero_name, health_points, age, race_id, is_alive=True):
        self.hero_name = hero_name
        self.health_points = health_points
        self.age = age
        self.race_id = race_id
        self.is_alive = is_alive

    def new_hero_obj():
        return Heros('', 0, 0, '', True)


class HerosSchema(ma.Schema):
    
    class Meta:
        fields = [ 'hero_id','hero_name','health_points', 'age', 'race', 'is_alive']

    hero_id = ma.fields.UUID()
    hero_name = ma.fields.String(required=True)
    health_points = ma.fields.Integer()
    age = ma.fields.Integer()
    is_alive = ma.fields.Boolean(allow_none=True, dump_default=True)

    race = ma.fields.Nested("RacesSchema")    
    
    
    
hero_schema = HerosSchema()
heros_schema = HerosSchema(many=True)