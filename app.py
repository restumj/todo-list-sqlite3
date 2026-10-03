from flask import *
import sqlite3

app = Flask(__name__)

def get_db_connection():
    db = sqlite3.connect('todo.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

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
        cu.execute('INSERT INTO tasks (name,status) VALUES (?,?)', (task_name,0))
        db.commit()
        new_id = cu.lastrowid
        db.close()
        return jsonify({'id': new_id, 'name': task_name, 'status': 0}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT','DELETE'])
def modify_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'PUT':
        data = request.get_json()
        new_status = data.get('status')
        cursor.execute('UPDATE tasks SET status = ? where id = ?', (new_status,task_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Status diperbarui','id': task_id,'status':new_status})
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM tasks WHERE id = ?',(task_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Tugas dihapus'})