from flask import *
import sqlite3

app = Flask(__name__)

def get_db_connection():
    db = sqlite3.connect('todo.db')
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET','POST'])
def handle_tasks():
    db = get_db_connection()

    if request.method == 'GET':
        tasks_cursor = db.execute('SELECT * FROM tasks').fetchall()
        db.close()
        tasks = [dict(row) for row in tasks_cursor]
        return jsonify(tasks)
    elif request.method == 'POST':
        data = request.get_json()
        task_name = data.get('name')
        cu = db.cursor()
        cu.execute('INSERT INTO tasks (name) VALUES (?)', (task_name))
        db.commit()
        new_id = cu.lastrowid
        db.close()
        return jsonify({'id': new_id, 'name': task_name, 'status': 0}), 201