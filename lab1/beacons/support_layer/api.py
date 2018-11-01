#!/usr/bin/env python
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.smart_building'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Beacon(db.Model):
    __tablename__ = "beacon"
    id = db.Column(db.Integer, primary_key=True)
    minor = db.Column(db.Text)
    room = db.Column(db.Integer)


class Blind(db.Model):
    __tablename__ = "blind"
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer)
    bloc = db.Column(db.Integer)
    room = db.Column(db.Integer)


class Radiator(db.Model):
    __tablename__ = "radiator"
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer)
    bloc = db.Column(db.Integer)
    room = db.Column(db.Integer)


class Sensor(db.Model):
    __tablename__ = "sensor"
    id = db.Column(db.Integer, primary_key=True)
    node = db.Column(db.Integer)
    room = db.Column(db.Integer)


class Light(db.Model):
    __tablename__ = "light"
    id = db.Column(db.Integer, primary_key=True)
    node = db.Column(db.Integer)
    room = db.Column(db.Integer)


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}


@app.route('/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/resource')
@auth.login_required
def get_resource():
    beacons = Beacon.query.all()
    beacons_list = []
    for b in beacons:
        beacons_list.append({
            'minor': b.minor,
            'room': b.room
        })

    blinds = Blind.query.all()
    blinds_list = []
    for b in blinds:
        blinds_list.append({
            'floor': b.floor,
            'bloc': b.bloc,
            'room': b.room
        })

    radiators = Radiator.query.all()
    radiators_list = []
    for b in radiators:
        radiators_list.append({
            'floor': b.floor,
            'bloc': b.bloc,
            'room': b.room
        })

    sensors = Sensor.query.all()
    sensors_list = []
    for b in sensors:
        sensors_list.append({
            'node': b.node,
            'room': b.room
        })

    lights = Light.query.all()
    lights_list = []
    for b in lights:
        lights_list.append({
            'node': b.node,
            'room': b.room
        })
    return jsonify({
        'beacons': beacons_list,
        'blinds': blinds_list,
        'radiators': radiators_list,
        'sensors': sensors_list,
        'lights': lights_list
    })


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=3003)
