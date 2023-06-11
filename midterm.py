import sqlite3
from unittest import result
from flask import Flask, render_template, jsonify, request, make_response
import random
import sys
import requests


app = Flask(__name__)
DB_FILE = "lux.sqlite"

def check_db():
    query = "SELECT distinct(id) FROM objects"
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return result
        return None

def get_object_from_db(obj_id=None):
    query = """select label, ifnull(date, 'Unknown'), 
                        ifnull(group_concat(name||'|'||part, '||'),'') as product, id from (
                        select o.id, o.label as label, o.date as date, a.name as name, p.part as part
                        from objects o
                        left outer join productions p on o.id = p.obj_id 
                        left outer join agents a on a.id = p.agt_id  
                        order by lower(p.part), lower(a.name)
                    ) where id=%s;
                """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            if not check_db():
                sys.exit("No objects in database")
            if obj_id is None:
                ids = check_db()
                obj_id = random.choice(ids)[0]
            query = query % obj_id
            print(query)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            return result
    except:
        return None


@app.route("/")
@app.route("/get_object")
@app.route("/get_previous_object")
def get_object(obj_id=None):
    if 'get_previous_object' in request.url:
        obj_id = request.cookies.get('previous_object')
    obj_info = get_object_from_db(obj_id)
    result = {"label": obj_info[0][0], "date": obj_info[0][1], "part": obj_info[0][2], "id": obj_info[0][3]}
    
    result['image'] = f"https://media.collections.yale.edu/thumbnail/yuag/obj/{result['id']}"
    response = requests.get(result['image'])
    if response.status_code != 200:
        result['image'] = None
    print(result)
    
    if 'get_object' in request.url or 'get_previous_object' in request.url:
        return jsonify(result)
    return render_template("index.html", obj = result)


