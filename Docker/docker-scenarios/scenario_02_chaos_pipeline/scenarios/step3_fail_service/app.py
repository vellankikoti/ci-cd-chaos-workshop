#!/usr/bin/env python3
import redis
import uuid
import time
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Try to connect to Redis (will fail in this scenario)
try:
    redis_client = redis.Redis(host='redis', port=6379, db=0, socket_connect_timeout=2)
    redis_client.ping()
    redis_available = True
except:
    redis_available = False

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy" if redis_available else "unhealthy",
        "step": "step3_fail_service",
        "message": "Session management service",
        "redis_available": redis_available,
        "service_dependencies": {
            "redis": redis_available
        }
    })

@app.route('/debug')
def debug():
    return jsonify({
        "step": "step3_fail_service",
        "description": "Service Dependency Failure Simulation",
        "service_status": {
            "redis_available": redis_available,
            "redis_host": "redis",
            "redis_port": 6379
        },
        "session_info": {
            "active_sessions": get_active_sessions_count(),
            "session_storage": "Redis" if redis_available else "In-memory (fallback)"
        },
        "educational_content": {
            "learning_objective": "Understanding service dependencies and microservices",
            "failure_mode": "Service dependency (Redis) is unavailable",
            "real_world_impact": "Applications fail when dependent services are down",
            "debugging_tips": [
                "Check service connectivity",
                "Verify service discovery",
                "Test service endpoints",
                "Implement fallback mechanisms"
            ]
        }
    })

@app.route('/run-experiment')
def run_experiment():
    """Run service dependency experiment"""
    results = {
        "experiment": "Service Dependency Test",
        "timestamp": time.time(),
        "tests": {
            "redis_connectivity": test_redis_connectivity(),
            "session_creation": test_session_creation(),
            "session_retrieval": test_session_retrieval()
        },
        "summary": "Service dependency experiment completed",
        "educational_value": "Demonstrates how microservices handle service dependencies"
    }
    
    return jsonify(results)

@app.route('/session/create', methods=['POST'])
def create_session():
    """Create a new session"""
    try:
        session_id = str(uuid.uuid4())
        session_data = {
            "id": session_id,
            "created_at": time.time(),
            "user_agent": request.headers.get('User-Agent', 'Unknown'),
            "data": request.json if request.is_json else {}
        }
        
        if redis_available:
            # Store in Redis
            redis_client.setex(f"session:{session_id}", 3600, json.dumps(session_data))
            storage_method = "Redis"
        else:
            # Store in memory (fallback)
            if not hasattr(app, 'sessions'):
                app.sessions = {}
            app.sessions[session_id] = session_data
            storage_method = "In-memory (fallback)"
        
        return jsonify({
            "status": "success",
            "session_id": session_id,
            "storage_method": storage_method,
            "message": "Session created successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Failed to create session"
        }), 500

@app.route('/session/<session_id>')
def get_session(session_id):
    """Get session by ID"""
    try:
        if redis_available:
            # Get from Redis
            session_data = redis_client.get(f"session:{session_id}")
            if session_data:
                session_data = json.loads(session_data)
                storage_method = "Redis"
            else:
                session_data = None
                storage_method = "Redis (not found)"
        else:
            # Get from memory (fallback)
            if hasattr(app, 'sessions') and session_id in app.sessions:
                session_data = app.sessions[session_id]
                storage_method = "In-memory (fallback)"
            else:
                session_data = None
                storage_method = "In-memory (not found)"
        
        if session_data:
            return jsonify({
                "status": "success",
                "session": session_data,
                "storage_method": storage_method
            })
        else:
            return jsonify({
                "status": "not_found",
                "session_id": session_id,
                "storage_method": storage_method
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Failed to retrieve session"
        }), 500

@app.route('/sessions')
def list_sessions():
    """List all active sessions"""
    try:
        if redis_available:
            # Get from Redis
            session_keys = redis_client.keys("session:*")
            sessions = []
            for key in session_keys:
                session_data = redis_client.get(key)
                if session_data:
                    sessions.append(json.loads(session_data))
            storage_method = "Redis"
        else:
            # Get from memory (fallback)
            sessions = list(getattr(app, 'sessions', {}).values())
            storage_method = "In-memory (fallback)"
        
        return jsonify({
            "status": "success",
            "sessions": sessions,
            "count": len(sessions),
            "storage_method": storage_method
        })
except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Failed to list sessions"
        }), 500

@app.route('/')
def index():
    return jsonify({
        "message": "Step 3: Service Failure",
        "description": "Session management service with Redis dependency",
        "redis_available": redis_available,
        "endpoints": {
            "health": "/health",
            "debug": "/debug",
            "experiment": "/run-experiment",
            "create_session": "/session/create (POST)",
            "get_session": "/session/<session_id>",
            "list_sessions": "/sessions"
        }
    })

def test_redis_connectivity():
    """Test Redis connectivity"""
    try:
        redis_client.ping()
        return True
    except:
        return False

def test_session_creation():
    """Test session creation"""
    try:
        session_id = str(uuid.uuid4())
        session_data = {"test": "data", "timestamp": time.time()}
        
        if redis_available:
            redis_client.setex(f"session:{session_id}", 60, json.dumps(session_data))
        else:
            if not hasattr(app, 'sessions'):
                app.sessions = {}
            app.sessions[session_id] = session_data
        
        return True
    except:
        return False

def test_session_retrieval():
    """Test session retrieval"""
    try:
        session_id = str(uuid.uuid4())
        session_data = {"test": "retrieval", "timestamp": time.time()}
        
        if redis_available:
            redis_client.setex(f"session:{session_id}", 60, json.dumps(session_data))
            retrieved = redis_client.get(f"session:{session_id}")
            return retrieved is not None
        else:
            if not hasattr(app, 'sessions'):
                app.sessions = {}
            app.sessions[session_id] = session_data
            return session_id in app.sessions
    except:
        return False

def get_active_sessions_count():
    """Get count of active sessions"""
    try:
        if redis_available:
            return len(redis_client.keys("session:*"))
        else:
            return len(getattr(app, 'sessions', {}))
    except:
        return 0

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
