import os
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, request

CREATE_ROOMS_TABLE = (
    "CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"
)
CREATE_TEMPS_TABLE = (
    """CREATE TABLE IF NOT EXISTS temperature (room_id INTEGER, temperature REAL,
        date TIMESTAMP, FORGEIN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""
)
INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"
INSERT_TEMPERATURE = (
    "INSERT INTO temperature (room_id, temperature, date) VALUES (%s, %s, %s);"
                      )
GLOBAL_NUMBER_OF_DAYS = (
    """(SELECT COUNT(DISTINCT date)) AS days FROM temperature;"""
)
GLOBAL_AVG = """SELECT AVG(temperature) as average FROM temperature;"""


load_dotenv()

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url)


@app.post('/api/room')
def create_room():
    data = request.get_json()
    name = data['name']
    with conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_ROOMS_TABLE)
            cur.execute(INSERT_ROOM_RETURN_ID, (name,))
            room_id = cur.fetchone()[0]
            return {'id': room_id, 'message': 'Room created successfully'}, 201


@app.post('/api//temperature')
def create_temperature():
    data = request.get_json()
    room = data['room']
    temperature = data['temperature']
    with conn.cursor() as cur:
        cur.execute(CREATE_TEMPS_TABLE)
    cur.execute(INSERT_TEMPERATURE, (room, temperature))
    return {'message': 'Temperature created successfully'}, 201








