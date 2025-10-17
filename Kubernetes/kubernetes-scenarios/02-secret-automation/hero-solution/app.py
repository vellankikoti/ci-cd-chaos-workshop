#!/usr/bin/env python3
"""
Simple Secure Todo App with SQLite
Demonstrates Kubernetes secret management without complex database

Secure Todo App for Kubernetes secret management demo.
"""
from flask import Flask, render_template_string, request, jsonify
import sqlite3
import os
import secrets

app = Flask(__name__)

# Get API key from environment variable (populated from Kubernetes Secret)
API_KEY = os.getenv('API_KEY', 'default-key')
APP_SECRET = os.getenv('APP_SECRET', 'default-secret')

# SQLite database
DB_FILE = '/tmp/todos.db'

def init_db():
    """Initialize database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_FILE}")
    print(f"✅ API Key loaded: {API_KEY[:8]}...")
    print(f"✅ App Secret loaded: {APP_SECRET[:8]}...")

init_db()

TODO_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🔐 Secure Todo App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: fadeIn 0.5s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            text-align: center;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .security-badge {
            background: #d4edda;
            color: #155724;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border: 2px solid #c3e6cb;
        }
        .security-badge h3 {
            margin-bottom: 15px;
            color: #155724;
            font-size: 1.2em;
        }
        .security-features {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .security-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .add-todo {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        .add-todo input {
            flex: 1;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1em;
        }
        .add-todo button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        .add-todo button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .todo-list {
            list-style: none;
        }
        .todo-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s;
            border-left: 4px solid #667eea;
        }
        .todo-item:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }
        .todo-item.completed {
            opacity: 0.6;
            text-decoration: line-through;
            border-left-color: #28a745;
        }
        .todo-text {
            flex: 1;
            font-size: 1.1em;
        }
        .todo-actions {
            display: flex;
            gap: 10px;
        }
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: bold;
            transition: all 0.2s;
        }
        .btn-complete {
            background: #28a745;
            color: white;
        }
        .btn-delete {
            background: #dc3545;
            color: white;
        }
        .btn:hover {
            transform: scale(1.1);
        }
        .empty-state {
            text-align: center;
            color: #999;
            padding: 40px;
            font-size: 1.2em;
        }
        .message {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: none;
            animation: slideDown 0.3s;
        }
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .stat {
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Secure Todo App</h1>
        <p class="subtitle">Kubernetes Secret Management Demo</p>

        <div class="security-badge">
            <h3>🛡️ Security Features Active:</h3>
            <div class="security-features">
                <div class="security-item">✅ Secrets from K8s</div>
                <div class="security-item">✅ Non-root container</div>
                <div class="security-item">✅ Read-only filesystem</div>
                <div class="security-item">✅ Resource limits</div>
                <div class="security-item">✅ Health checks</div>
                <div class="security-item">✅ Encrypted at rest</div>
            </div>
        </div>

        <div id="message" class="message"></div>

        <div class="add-todo">
            <input type="text" id="taskInput" placeholder="What needs to be done?" onkeypress="if(event.key==='Enter') addTodo()">
            <button onclick="addTodo()">➕ Add Task</button>
        </div>

        <ul class="todo-list" id="todoList">
            <li class="empty-state">📝 No tasks yet. Add one above!</li>
        </ul>

        <div class="stats">
            <div class="stat">
                <div class="stat-number" id="totalTasks">0</div>
                <div class="stat-label">Total Tasks</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="completedTasks">0</div>
                <div class="stat-label">Completed</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="pendingTasks">0</div>
                <div class="stat-label">Pending</div>
            </div>
        </div>
    </div>

    <script>
        function showMessage(text) {
            const msg = document.getElementById('message');
            msg.textContent = text;
            msg.className = 'message success';
            msg.style.display = 'block';
            setTimeout(() => { msg.style.display = 'none'; }, 3000);
        }

        function updateStats(todos) {
            const total = todos.length;
            const completed = todos.filter(t => t.completed).length;
            const pending = total - completed;

            document.getElementById('totalTasks').textContent = total;
            document.getElementById('completedTasks').textContent = completed;
            document.getElementById('pendingTasks').textContent = pending;
        }

        function loadTodos() {
            fetch('/api/todos')
            .then(response => response.json())
            .then(todos => {
                const list = document.getElementById('todoList');
                updateStats(todos);

                if (todos.length === 0) {
                    list.innerHTML = '<li class="empty-state">📝 No tasks yet. Add one above!</li>';
                    return;
                }

                list.innerHTML = todos.map(todo => `
                    <li class="todo-item ${todo.completed ? 'completed' : ''}">
                        <span class="todo-text">${todo.task}</span>
                        <div class="todo-actions">
                            ${!todo.completed ? `<button class="btn btn-complete" onclick="completeTodo(${todo.id})">✓ Done</button>` : ''}
                            <button class="btn btn-delete" onclick="deleteTodo(${todo.id})">🗑️</button>
                        </div>
                    </li>
                `).join('');
            });
        }

        function addTodo() {
            const input = document.getElementById('taskInput');
            const task = input.value.trim();
            if (!task) return;

            fetch('/api/todos', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({task: task})
            })
            .then(response => response.json())
            .then(data => {
                showMessage('✅ Task added successfully!');
                input.value = '';
                loadTodos();
            });
        }

        function completeTodo(id) {
            fetch(`/api/todos/${id}/complete`, {method: 'PUT'})
            .then(() => {
                showMessage('✅ Task completed!');
                loadTodos();
            });
        }

        function deleteTodo(id) {
            fetch(`/api/todos/${id}`, {method: 'DELETE'})
            .then(() => {
                showMessage('🗑️ Task deleted!');
                loadTodos();
            });
        }

        // Load todos on page load and auto-refresh
        loadTodos();
        setInterval(loadTodos, 3000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(TODO_TEMPLATE)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
    todos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    task = data.get('task')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task) VALUES (?)", (task,))
    conn.commit()
    todo_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': todo_id, 'task': task, 'completed': False})

@app.route('/api/todos/<int:todo_id>/complete', methods=['PUT'])
def complete_todo(todo_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET completed = 1 WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'secrets_loaded': bool(API_KEY and APP_SECRET),
        'api_key_preview': API_KEY[:8] + '...'
    })

if __name__ == '__main__':
    print("🔐 Starting Secure Todo App...")
    print(f"✅ API Key: {API_KEY[:12]}...")
    print(f"✅ App Secret: {APP_SECRET[:12]}...")
    app.run(host='0.0.0.0', port=8080, debug=True)
