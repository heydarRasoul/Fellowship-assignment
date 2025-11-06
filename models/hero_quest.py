import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class HeroQuests(db.Model):
    __tablename__ = 'HeroQuests'

    hero_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Heros.hero_id'), primary_key=True, default=uuid.uuid4)
    quest_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Quests.quest_id'), primary_key=True, default=uuid.uuid4)
    date_joined= db.Column(db.DateTime)

    heros = db.relationship("Heros", back_populates="heroQuests")
    quests = db.relationship("Quests", back_populates="heroQuests")

    def __init__(self,hero_id, quest_id, date_joined):
        self.hero_id=hero_id
        self.quest_id=quest_id
        self.date_joined=date_joined

    def new_hero_quest_obj():
        return HeroQuests('','','')
    
class HeroQuestsSchema(ma.Schema):
    class Meta:
        fields = ['hero','quest','date_joined']
   
   
    date_joined = ma.fields.DateTime()
  
    hero = ma.fields.Nested("HerosSchema") 
    quest = ma.fields.Nested("QuestsSchema") 

heroQuest_schema = HeroQuestsSchema()
heroQuests_schema = HeroQuestsSchema(many=True)