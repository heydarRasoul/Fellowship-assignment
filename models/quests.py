import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .hero_quest import HeroQuests


class Quests(db.Model):
    __tablename__ = "Quests"

    quest_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quest_name = db.Column(db.String(), nullable=False, unique=True)
    difficulty = db.Column(db.String())
    reward_gold = db.Column(db.Integer())
    is_completed = db.Column(db.Boolean(), default=False)
    location_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Locations.location_id"), nullable=False)

    location = db.relationship("Locations", foreign_keys='[Quests.location_id]', back_populates='quests')
    heroQuests = db.relationship("HeroQuests", back_populates="quests", cascade="all")

    def __init__(self, quest_name, difficulty, reward_gold, location_id, is_completed=True):
        self.quest_name = quest_name
        self.difficulty = difficulty
        self.reward_gold = reward_gold
        self.location_id = location_id
        self.is_completed = is_completed

    def new_quest_obj():
        return Quests('', '', '', 0, True)


class QuestsSchema(ma.Schema):
    
    class Meta:
        fields = ['quest_id', 'quest_name', 'difficulty', 'reward_gold', 'location', 'is_completed']

    quest_id = ma.fields.UUID()
    quest_name = ma.fields.String(required=True)
    difficulty = ma.fields.String(allow_none=True)
    reward_gold = ma.fields.Integer(allow_none=True)
    is_completed = ma.fields.Boolean(allow_none=True, dump_default=False)

    location = ma.fields.Nested("LocationsSchema")    
   
    
quest_schema = QuestsSchema()
quests_schema = QuestsSchema(many=True)