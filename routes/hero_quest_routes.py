
from flask import Blueprint

import controllers

hero_quest = Blueprint('hero_quest', __name__)

@hero_quest.route('/hero-quest', methods=['POST'])
def add_hero_to_quest_route():
    return controllers.add_hero_to_quest()


