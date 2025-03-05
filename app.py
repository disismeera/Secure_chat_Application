from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, emit
from cryptography.fernet import Fernet
import sqlite3
import uuid
import html

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Required for SocketIO
socketio = SocketIO(app)
key = Fernet.generate_key()  # Store securely in production
cipher = Fernet(key)

# Initialize database
def init_db():
    conn = sqlite3.connect('chats.db')
    conn.execute('CREATE TABLE IF NOT EXISTS rooms (code TEXT PRIMARY KEY, name TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, room_code TEXT, sender TEXT, message TEXT)')
    conn.close()

# Enter name page
@app.route('/', methods=['GET', 'POST'])
def enter_name():
    if request.method == 'POST':
        name = request.form['name'].strip()
        if name:
            return redirect(url_for('options', name=name))
        return render_template('enter_name.html', error="Name cannot be empty!")
    return render_template('enter_name.html', error=None)

# Options page
@app.route('/options/<name>')
def options(name):
    return render_template('options.html', name=name)

# Start new chat
@app.route('/new_chat/<name>', methods=['GET', 'POST'])
def new_chat(name):
    if request.method == 'POST':
        code = str(uuid.uuid4())[:8]  # Shortened unique code
        conn = sqlite3.connect('chats.db')
        conn.execute('INSERT INTO rooms (code, name) VALUES (?, ?)', (code, f"Chat by {name}"))
        conn.commit()
        conn.close()
        return redirect(url_for('chat_room', code=code, name=name))
    return render_template('new_chat.html', name=name)

# Join chat
@app.route('/join_chat/<name>', methods=['GET', 'POST'])
def join_chat(name):
    if request.method == 'POST':
        code = request.form['code'].strip()
        conn = sqlite3.connect('chats.db')
        cursor = conn.execute('SELECT code FROM rooms WHERE code = ?', (code,))
        if cursor.fetchone():
            conn.close()
            return redirect(url_for('chat_room', code=code, name=name))
        conn.close()
        return render_template('join_chat.html', name=name, error="Invalid code!")
    return render_template('join_chat.html', name=name, error=None)

# Chat room
@app.route('/chat/<code>/<name>')
def chat_room(code, name):
    conn = sqlite3.connect('chats.db')
    cursor = conn.execute('SELECT code FROM rooms WHERE code = ?', (code,))
    if not cursor.fetchone():
        conn.close()
        return "Chat room not found!"
    
    cursor = conn.execute('SELECT sender, message FROM messages WHERE room_code = ?', (code,))
    encrypted_messages = cursor.fetchall()
    messages = [(sender, cipher.decrypt(msg.encode()).decode()) for sender, msg in encrypted_messages]
    conn.close()
    return render_template('chat_room.html', code=code, name=name, messages=messages)

# SocketIO event for sending messages
@socketio.on('send_message')
def handle_message(data):
    code = data['code']
    name = data['name']
    message = html.escape(data['message'].strip())
    if message:
        encrypted_msg = cipher.encrypt(message.encode()).decode()
        conn = sqlite3.connect('chats.db')
        conn.execute('INSERT INTO messages (room_code, sender, message) VALUES (?, ?, ?)', (code, name, encrypted_msg))
        conn.commit()
        conn.close()
        # Broadcast the decrypted message to all in the room
        emit('new_message', {'sender': name, 'message': message}, room=code)

# SocketIO event for joining a room
@socketio.on('join')
def on_join(data):
    code = data['code']
    join_room(code)

if __name__ == '__main__':
    init_db()
    socketio.run(app, debug=True)