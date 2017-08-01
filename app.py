import sqlite3
import json
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/api/comedy', methods=['GET', 'POST'])
def collection():
    if request.method == 'GET':
        all_comedians = get_all_comedians()
        return json.dumps(all_comedians)
    elif request.method == 'POST':
        data = request.form
        result = add_comedian(data['comedian'], data['album'], data['rating'])
        return jsonify(result)


@app.route('/api/comedian/<comedian_id>', methods=['GET', 'PUT', 'DELETE'])
def resource(comedian_id):
    if request.method == 'GET':
        comedian = get_one_comedian(comedian_id)
        return json.dumps(comedian)
    elif request.method == 'PUT':
        data = request.form
        result = edit_comedian(
            comedian_id, data['comedian'], data['album'], data['rating'])
        return jsonify(result)
    elif request.method == 'DELETE':
        result = delete_comedian(comedian_id)
        return jsonify(result)


# helper functions

def add_comedian(comedian, album, rating):
    try:
        with sqlite3.connect('comedy.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO comedy (comedian, album, rating) values (?, ?, ?);
                """, (comedian, album, rating,))
            result = {'status': 1, 'message': 'Comedian Added'}
    except:
        result = {'status': 0, 'message': 'error'}
    return result

def get_all_comedians():
    with sqlite3.connect('comedy.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM comedy ORDER BY id desc")
        all_comedians = cursor.fetchall()
        return all_comedians

def get_one_comedian(comedian_id):
    with sqlite3.connect('comedy.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM comedy WHERE id = ?", (comedian_id,))
        comedian = cursor.fetchone()
        return comedian

def edit_comedian(comedian_id, comedian, album, rating):
    try:
        with sqlite3.connect('comedy.db') as connection:
            connection.execute("UPDATE comedy SET comedian = ?, album = ?, rating = ? WHERE ID = ?;", (comedian, album, rating, comedian_id,))
            result = {'status': 1, 'message': 'COMEDIAN Edited'}
    except:
        result = {'status': 0, 'message': 'Error'}
    return result

def delete_comedian(comedian_id):
    try:
        with sqlite3.connect('comedy.db') as connection:
            connection.execute("DELETE FROM comedy WHERE ID = ?;", (comedian_id,))
            result = {'status': 1, 'message': 'COMEDIAN Deleted'}
    except:
        result = {'status': 0, 'message': 'Error'}
    return result

if __name__ == '__main__':
    app.debug = True
    app.run()
