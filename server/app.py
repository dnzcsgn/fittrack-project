import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

# load env variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# jwt secret coming from .env file
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# workout table
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    duration = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

# simple home route just to check backend is running
@app.route("/")
def home():
    return jsonify({"message": "FitTrack API running"})

# register new user
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json

    # check if user already exists
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "user already exists"}), 400

    # hash password before saving
    hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(username=data["username"], password=hashed)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "user created"}), 201

# login user and give token
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(username=data["username"]).first()

    # simple login check
    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"error": "invalid login"}), 401

    # create jwt token
    token = create_access_token(identity=str(user.id))

    return jsonify({"token": token})

# get all workouts for logged user
@app.route("/api/workouts", methods=["GET"])
@jwt_required()
def get_workouts():
    user_id = get_jwt_identity()

    workouts = Workout.query.filter_by(user_id=user_id).all()

    return jsonify([
        {"id": w.id, "title": w.title, "duration": w.duration}
        for w in workouts
    ])

# add new workout
@app.route("/api/workouts", methods=["POST"])
@jwt_required()
def add_workout():
    user_id = get_jwt_identity()
    data = request.json

    # simple validation
    if not data:
        return jsonify({"error": "missing data"}), 400

    workout = Workout(
        title=data["title"],
        duration=data["duration"],
        user_id=user_id
    )

    db.session.add(workout)
    db.session.commit()

    return jsonify({
        "id": workout.id,
        "title": workout.title,
        "duration": workout.duration
    }), 201

# delete workout (only owner can delete)
@app.route("/api/workouts/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_workout(id):
    user_id = get_jwt_identity()

    workout = Workout.query.filter_by(id=id, user_id=user_id).first()

    if not workout:
        return jsonify({"error": "not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "deleted"})

# run server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(port=5555, debug=True)