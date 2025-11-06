

from routes.abilities_routes import ability
from routes.heros_routes import hero
from routes.location_routes import location
from routes.quests_routes import quest
from routes.races_routes import race
from routes.realms_routes import realm


def register_blueprints(app):
    app.register_blueprint(ability)
    app.register_blueprint(hero)
    app.register_blueprint(location)
    app.register_blueprint(quest)
    app.register_blueprint(race)
    app.register_blueprint(realm)