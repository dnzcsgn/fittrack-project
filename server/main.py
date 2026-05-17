from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from config import db, migrate, bcrypt, jwt
from models import User, Workout

app = Flask(__name__)

# basic config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"

CORS(app)

db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)


# register new user

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json

    user = User(username=data["username"])
    user.password = data["password"]

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201



# login user

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(username=data["username"]).first()

    if user and user.authenticate(data["password"]):

        token = create_access_token(identity=user.id)

        return jsonify({
            "token": token,
            "user": user.to_dict()
        })

    return jsonify({"error": "invalid login"}), 401



# get workouts for user

@app.route("/api/workouts", methods=["GET"])
@jwt_required()
def get_workouts():
    user_id = get_jwt_identity()

    workouts = Workout.query.filter_by(user_id=user_id).all()

    return jsonify([w.to_dict() for w in workouts])



# create workout

@app.route("/api/workouts", methods=["POST"])
@jwt_required()
def create_workout():
    user_id = get_jwt_identity()
    data = request.json

    workout = Workout(
        title=data["title"],
        duration=data["duration"],
        user_id=user_id
    )

    db.session.add(workout)
    db.session.commit()

    return jsonify(workout.to_dict()), 201



# delete workout (only owner)

@app.route("/api/workouts/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_workout(id):
    user_id = get_jwt_identity()

    workout = Workout.query.get(id)

    if not workout:
        return jsonify({"error": "not found"}), 404

    if workout.user_id != user_id:
        return jsonify({"error": "unauthorized"}), 403

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "deleted"})


# update workout

@app.route("/api/workouts/<int:id>", methods=["PATCH"])
@jwt_required()
def update_workout(id):
    user_id = get_jwt_identity()

    workout = Workout.query.get(id)

    if not workout:
        return jsonify({"error": "not found"}), 404

    if workout.user_id != user_id:
        return jsonify({"error": "unauthorized"}), 403

    data = request.json

    workout.title = data["title"]
    workout.duration = data["duration"]

    db.session.commit()

    return jsonify(workout.to_dict())


if __name__ == "__main__":
    app.run(port=5555, debug=True)