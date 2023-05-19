"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, session
from api.models import db, User, Location, Character, Episode, Favorite
from api.utils import generate_sitemap, APIException

api = Blueprint("api", __name__)

@api.route("/character", methods=["GET"])
def get_all_characters():
    characters = Character.query.all()

    char_serialized = [character.serialize() for character in characters]

    return jsonify({"characters": char_serialized}), 200


@api.route("/character/<int:character_id>", methods=["GET"])
def get_character_by_id(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "No character found with this id"}), 400
    return jsonify({"character": character.serialize()}), 200


@api.route("/location", methods=["GET"])
def get_all_locations():
    locations = Location.query.all()

    location_serialized = [location.serialize() for location in locations]

    return jsonify({"locations": location_serialized}), 200


@api.route("/location/<int:location_id>", methods=["GET"])
def get_location_by_id(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({"error": "No location found with this id"}), 400
    return jsonify({"location": location.serialize()}), 200


@api.route("/episode", methods=["GET"])
def get_all_episodes():
    episodes = Episode.query.all()

    episode_serialized = [episode.serialize() for episode in episodes]
    print("@@@@@@@@@@@@@@@@@@@")
    print(episodes)
    print(episode_serialized)
    print("@@@@@@@@@@@@@@@@@@@")

    return jsonify({"episodes": episode_serialized}), 200


@api.route("/episode/<int:episode_id>", methods=["GET"])
def get_episode_by_id(episode_id):
    episode = Episode.query.get(episode_id)
    if not episode:
        return jsonify({"error": "No episode found with this id"}), 400
    return jsonify({"episode": episode.serialize()}), 200


@api.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()

    user_serialized = [user.serialize() for user in users]
    print("@@@@@@@@@@@@@@@@@@@")
    print(users)
    print(user_serialized)
    print("@@@@@@@@@@@@@@@@@@@")

    return jsonify({"users": user_serialized}), 200



@api.route("/users/favorites/<int:user_id>", methods=["GET"])
def get_all_user_favorites_by_user_id(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()

    favorites_serialized = [favorite.serialize() for favorite in favorites]
    print("@@@@@@@@@@@@@@@@@@@")
    print(favorites)
    print("@@@@@@@@@@@@@@@@@@@")

    return jsonify({"favorites": favorites_serialized}), 200


@api.route("/favorite/character/<int:character_id>", methods=["POST"])
def add_favorite_character(character_id):
    user_id = 1

    character = Character.query.get(character_id)
    if not character and character != "undefined" and character != '':
        return jsonify({"error": "Character does not exist"}), 400
    
    body = request.json
    favorite_character = Favorite(
        user_id=user_id, 
        character_id=body["character_id"])

    db.session.add(favorite_character)
    db.session.commit()

    return jsonify({"message": "Favorite character added successfully"}), 200


@api.route("/favorite/episode/<int:episode_id>", methods=["POST"])
def add_favorite_episode(episode_id):
    user_id = 1

    episode = Episode.query.get(episode_id)
    if not episode and episode != "undefined" and episode != '':
        return jsonify({"error": "Episode does not exist"}), 400
    
    body = request.json
    favorite_episode = Favorite(
        user_id=user_id, 
        episode_id=body["episode_id"])

    db.session.add(favorite_episode)
    db.session.commit()

    return jsonify({"message": "Favorite episode added successfully"}), 200


@api.route("/favorite/location/<int:location_id>", methods=["POST"])
def add_favorite_location(location_id):
    user_id = 1

    location = Location.query.get(location_id)
    if not location and location != "undefined" and location != '':
        return jsonify({"error": "Location does not exist"}), 400
    
    body = request.json
    favorite_location = Favorite(
        user_id=user_id, 
        location_id=body["location_id"])

    db.session.add(favorite_location)
    db.session.commit()

    return jsonify({"message": "Favorite location added successfully"}), 200


@api.route("/favorite/character/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "No character found with this id"}), 400
    db.session.delete(character)
    db.session.commit()
    return jsonify("character deleted"), 200


@api.route("/favorite/episode/<int:episode_id>", methods=["DELETE"])
def delete_episode(episode_id):
    episode = Episode.query.get(episode_id)
    if not episode:
        return jsonify({"error": "No episode found with this id"}), 400
    db.session.delete(episode)
    db.session.commit()
    return jsonify("episode deleted"), 200


@api.route("/favorite/location/<int:location_id>", methods=["DELETE"])
def delete_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({"error": "No location found with this id"}), 400
    db.session.delete(location)
    db.session.commit()
    return jsonify("location deleted"), 200
