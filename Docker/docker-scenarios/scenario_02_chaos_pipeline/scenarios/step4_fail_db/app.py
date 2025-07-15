#!/usr/bin/env python3
import pymysql
import time
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Try to connect to MySQL (will fail in this scenario)
try:
    mysql_connection = pymysql.connect(
        host='mysql',
        port=3306,
        user='root',
        password='password',
        database='test',
        connect_timeout=2
    )
    mysql_available = True
except:
    mysql_available = False

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy" if mysql_available else "unhealthy",
        "step": "step4_fail_db",
        "message": "User management service",
        "mysql_available": mysql_available,
        "database_dependencies": {
            "mysql": mysql_available
        }
    })

@app.route('/debug')
def debug():
    return jsonify({
        "step": "step4_fail_db",
        "description": "Database Connectivity Failure Simulation",
        "database_status": {
            "mysql_available": mysql_available,
            "mysql_host": "mysql",
            "mysql_port": 3306,
            "mysql_database": "test"
        },
        "user_info": {
            "total_users": get_users_count(),
            "database_storage": "MySQL" if mysql_available else "In-memory (fallback)"
        },
        "educational_content": {
            "learning_objective": "Understanding database dependencies and persistence",
            "failure_mode": "Database connection fails - MySQL is not running",
            "real_world_impact": "Applications fail when database is unavailable",
            "debugging_tips": [
                "Check database connectivity",
                "Verify database credentials",
                "Test database queries",
                "Implement connection pooling"
            ]
        }
    })

@app.route('/run-experiment')
def run_experiment():
    """Run database connectivity experiment"""
    results = {
        "experiment": "Database Connectivity Test",
        "timestamp": time.time(),
        "tests": {
            "mysql_connectivity": test_mysql_connectivity(),
            "user_creation": test_user_creation(),
            "user_retrieval": test_user_retrieval()
        },
        "summary": "Database connectivity experiment completed",
        "educational_value": "Demonstrates how applications handle database failures"
    }
    
    return jsonify(results)

@app.route('/user/create', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        user_data = request.json if request.is_json else {}
        user_id = f"user_{int(time.time())}"
        
        user_info = {
            "id": user_id,
            "name": user_data.get('name', 'Anonymous'),
            "email": user_data.get('email', f'{user_id}@example.com'),
            "created_at": time.time(),
            "status": "active"
        }
        
        if mysql_available:
            # Store in MySQL
            with mysql_connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id VARCHAR(50) PRIMARY KEY,
                        name VARCHAR(100),
                        email VARCHAR(100),
                        created_at TIMESTAMP,
                        status VARCHAR(20)
                    )
                """)
                
                cursor.execute("""
                    INSERT INTO users (id, name, email, created_at, status)
                    VALUES (%s, %s, %s, FROM_UNIXTIME(%s), %s)
                """, (user_info['id'], user_info['name'], user_info['email'], 
                     user_info['created_at'], user_info['status']))
                
                mysql_connection.commit()
            storage_method = "MySQL"
        else:
            # Store in memory (fallback)
            if not hasattr(app, 'users'):
                app.users = {}
            app.users[user_id] = user_info
            storage_method = "In-memory (fallback)"
        
        return jsonify({
            "status": "success",
            "user": user_info,
            "storage_method": storage_method,
            "message": "User created successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Failed to create user"
        }), 500

@app.route('/user/<user_id>')
def get_user(user_id):
    """Get user by ID"""
    try:
        if mysql_available:
            # Get from MySQL
            with mysql_connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user_data = cursor.fetchone()
                storage_method = "MySQL"
        else:
            # Get from memory (fallback)
            user_data = getattr(app, 'users', {}).get(user_id)
            storage_method = "In-memory (fallback)"
        
        if user_data:
            return jsonify({
                "status": "success",
                "user": user_data,
                "storage_method": storage_method
            })
        else:
            return jsonify({
                "status": "not_found",
                "user_id": user_id,
                "storage_method": storage_method
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Failed to retrieve user"
        }), 500

@app.route('/users')
def list_users():
    """List all users"""
    try:
        if mysql_available:
            # Get from MySQL
            with mysql_connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
                users = cursor.fetchall()
            storage_method = "MySQL"
        else:
            # Get from memory (fallback)
            users = list(getattr(app, 'users', {}).values())
            storage_method = "In-memory (fallback)"
        
        return jsonify({
            "status": "success",
            "users": users,
            "count": len(users),
            "storage_method": storage_method
        })
except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Failed to list users"
        }), 500

@app.route('/')
def index():
    return jsonify({
        "message": "Step 4: Database Failure",
        "description": "User management service with MySQL dependency",
        "mysql_available": mysql_available,
        "endpoints": {
            "health": "/health",
            "debug": "/debug",
            "experiment": "/run-experiment",
            "create_user": "/user/create (POST)",
            "get_user": "/user/<user_id>",
            "list_users": "/users"
        }
    })

def test_mysql_connectivity():
    """Test MySQL connectivity"""
    try:
        mysql_connection.ping()
        return True
    except:
        return False

def test_user_creation():
    """Test user creation"""
    try:
        user_id = f"test_user_{int(time.time())}"
        user_data = {
            "id": user_id,
            "name": "Test User",
            "email": f"{user_id}@test.com",
            "created_at": time.time(),
            "status": "active"
        }
        
        if mysql_available:
            with mysql_connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (id, name, email, created_at, status)
                    VALUES (%s, %s, %s, FROM_UNIXTIME(%s), %s)
                """, (user_data['id'], user_data['name'], user_data['email'], 
                     user_data['created_at'], user_data['status']))
                mysql_connection.commit()
        else:
            if not hasattr(app, 'users'):
                app.users = {}
            app.users[user_id] = user_data
        
        return True
    except:
        return False

def test_user_retrieval():
    """Test user retrieval"""
    try:
        user_id = f"test_retrieval_{int(time.time())}"
        user_data = {
            "id": user_id,
            "name": "Test Retrieval",
            "email": f"{user_id}@test.com",
            "created_at": time.time(),
            "status": "active"
        }
        
        if mysql_available:
            with mysql_connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (id, name, email, created_at, status)
                    VALUES (%s, %s, %s, FROM_UNIXTIME(%s), %s)
                """, (user_data['id'], user_data['name'], user_data['email'], 
                     user_data['created_at'], user_data['status']))
                mysql_connection.commit()
                
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                retrieved = cursor.fetchone()
                return retrieved is not None
        else:
            if not hasattr(app, 'users'):
                app.users = {}
            app.users[user_id] = user_data
            return user_id in app.users
    except:
        return False

def get_users_count():
    """Get count of users"""
    try:
        if mysql_available:
            with mysql_connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM users")
                return cursor.fetchone()[0]
        else:
            return len(getattr(app, 'users', {}))
    except:
        return 0

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
