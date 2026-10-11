from flask import * 
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'CWZMdR_HjQhv'
app.permanent_session_lifetime = timedelta(minutes=30)

def get_db_connection():
    db = sqlite3.connect('todo.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status INTEGER DEFAULT 0,
            user_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/') 
def home():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template('index.html', username=session['username'])

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username,password) VALUES (?,?)', (username,hashed_password))
            conn.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return 'The username already exists.'
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password_input):
            session.permanent = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/')
        else:
            return 'Username or password is wrong.'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/api/tasks', methods=['GET','POST'])
def handle_tasks():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    db = get_db_connection()

    if request.method == 'GET':
        tasks_cursor = db.execute('SELECT * FROM tasks WHERE user_id=?',(user_id,)).fetchall()
        db.close()
        tasks = [dict(row) for row in tasks_cursor]
        return jsonify(tasks)
    elif request.method == 'POST':
        data = request.get_json()
        task_name = data.get('name')
        cu = db.cursor()
        cu.execute('INSERT INTO tasks (name,status,user_id) VALUES (?,?,?)', (task_name,0,user_id))
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
        cursor.execute('DELETE FROM tasks WHERE id = ?',(task_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Tugas dihapus'})