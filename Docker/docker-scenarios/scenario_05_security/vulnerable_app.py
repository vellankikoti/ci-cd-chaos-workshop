from flask import Flask, render_template_string, request, jsonify
import os
import time
import logging
import subprocess
import json
import base64

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 🚨 VULNERABLE SECURITY ANTI-PATTERNS - DO NOT USE IN PRODUCTION!
# These are intentionally vulnerable for educational purposes
#
# This file demonstrates what NOT to do in production.
# Compare with secure_app.py to see the proper security implementation.

# Hardcoded secrets (BAD!)
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"
SECRET_KEY = "super-secret-key-123"
JWT_SECRET = "jwt-secret-key-456"

# Hardcoded database credentials
DB_HOST = "localhost"
DB_USER = "admin"
DB_PASS = "password123"
DB_NAME = "vulnerable_db"

# Hardcoded API endpoints
EXTERNAL_API_URL = "https://api.vulnerable-service.com"
API_TOKEN = "token-abc123def456"

TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>🚨 Vulnerable Docker App</title>
    <style>
        body {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
            font-family: 'Segoe UI', 'Arial', sans-serif;
            text-align: center;
            padding: 0;
            margin: 0;
            min-height: 100vh;
            color: white;
        }
        .container {
            margin-top: 60px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31,38,135,0.3);
            display: inline-block;
            padding: 40px 60px;
            max-width: 900px;
            width: 90%;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        h1 {
            font-size: 3em;
            margin-bottom: 0.2em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            font-size: 1.3em;
            margin-bottom: 2em;
            opacity: 0.9;
        }
        .warning-box {
            background: rgba(255,255,255,0.2);
            border-left: 5px solid #ffeb3b;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            text-align: left;
        }
        .danger-box {
            background: rgba(255,0,0,0.3);
            border-left: 5px solid #f44336;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            text-align: left;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .stat {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
            color: #ffeb3b;
        }
        .stat-label {
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.8;
        }
        .vulnerabilities-list {
            text-align: left;
            margin: 20px 0;
        }
        .vulnerabilities-list li {
            margin: 10px 0;
            padding: 5px;
        }
        .footer {
            margin-top: 40px;
            color: rgba(255,255,255,0.7);
            font-size: 0.9em;
        }
        .pulse {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        .secret-exposed {
            background: rgba(255,0,0,0.2);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-family: monospace;
            word-break: break-all;
        }
        .user-info {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            text-align: left;
        }
        .danger {
            color: #ff6b6b;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚨 VULNERABLE DOCKER APP</h1>
        <div class="subtitle">This is what NOT to do in production!</div>
        
        <div class="danger-box">
            <h3>⚠️ CRITICAL SECURITY WARNING</h3>
            <p>This container demonstrates common Docker security mistakes that lead to massive security vulnerabilities and data breaches.</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value pulse">0%</div>
                <div class="stat-label">Security Score</div>
            </div>
            <div class="stat">
                <div class="stat-value pulse">15+</div>
                <div class="stat-label">Vulnerabilities</div>
            </div>
            <div class="stat">
                <div class="stat-value pulse">🔴</div>
                <div class="stat-label">Critical Risk</div>
            </div>
            <div class="stat">
                <div class="stat-value pulse">ROOT</div>
                <div class="stat-label">User</div>
            </div>
        </div>
        
        <div class="warning-box">
            <h3>🔓 Exposed Secrets (DO NOT DO THIS!):</h3>
            <div class="secret-exposed">
                <strong>Database Password:</strong> {{ db_password }}<br>
                <strong>API Key:</strong> {{ api_key }}<br>
                <strong>Secret Key:</strong> {{ secret_key }}<br>
                <strong>JWT Secret:</strong> {{ jwt_secret }}
            </div>
        </div>
        
        <div class="user-info">
            <h3>👤 Current User Information:</h3>
            <p><strong>User ID:</strong> {{ user_id }}</p>
            <p><strong>Username:</strong> {{ username }}</p>
            <p><strong>Group ID:</strong> {{ group_id }}</p>
            <p><strong>Is Root:</strong> <span class="danger">{{ is_root }}</span></p>
            <p><strong>Home Directory:</strong> {{ home_dir }}</p>
        </div>
        
        <div class="warning-box">
            <h3>🐛 Critical Security Vulnerabilities:</h3>
            <div class="vulnerabilities-list">
                <ul>
                    <li>🔴 Hardcoded secrets in source code - data breach risk</li>
                    <li>🔴 Running as root user - privilege escalation</li>
                    <li>🔴 No network isolation - lateral movement risk</li>
                    <li>🔴 Exposed environment variables - credential theft</li>
                    <li>🔴 No secrets management - compliance violations</li>
                    <li>🔴 No security scanning - unknown vulnerabilities</li>
                    <li>🔴 No user restrictions - container escape risk</li>
                    <li>🔴 No resource limits - DoS attacks possible</li>
                    <li>🔴 No health checks - service degradation</li>
                    <li>🔴 No logging security - audit trail missing</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🎯 Compare with:</strong></p>
            <p><a href="http://localhost:8002" style="color: #4ecdc4;">🔒 Secure App (100% Security Score)</a></p>
            <p><a href="http://localhost:8000" style="color: #667eea;">📊 Live Security Dashboard</a></p>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    """Vulnerable app demonstration page"""
    logger.info("🚨 Vulnerable app accessed - demonstrating security anti-patterns")
    
    # Get current user information (shows root user vulnerability)
    try:
        user_id = os.getuid()
        username = os.getenv('USER', 'root')
        group_id = os.getgid()
        is_root = "YES" if user_id == 0 else "NO"
        home_dir = os.path.expanduser('~')
    except Exception as e:
        user_id = "Unknown"
        username = "root"
        group_id = "Unknown"
        is_root = "YES"
        home_dir = "/root"
    
    return render_template_string(TEMPLATE, 
        db_password=DATABASE_PASSWORD,
        api_key=API_KEY,
        secret_key=SECRET_KEY,
        jwt_secret=JWT_SECRET,
        user_id=user_id,
        username=username,
        group_id=group_id,
        is_root=is_root,
        home_dir=home_dir
    )

@app.route("/health")
def health():
    """Health check endpoint - shows security issues"""
    return {
        "status": "vulnerable", 
        "security_score": 0,
        "vulnerabilities": 15,
        "user": "root",
        "secrets_exposed": True,
        "timestamp": time.time()
    }

@app.route("/secrets")
def secrets():
    """Dangerous endpoint that exposes all secrets (DO NOT DO THIS!)"""
    return {
        "database_password": DATABASE_PASSWORD,
        "api_key": API_KEY,
        "secret_key": SECRET_KEY,
        "jwt_secret": JWT_SECRET,
        "db_host": DB_HOST,
        "db_user": DB_USER,
        "db_pass": DB_PASS,
        "external_api_url": EXTERNAL_API_URL,
        "api_token": API_TOKEN,
        "warning": "🚨 NEVER expose secrets like this in production!"
    }

@app.route("/system")
def system_info():
    """Dangerous endpoint that exposes system information"""
    try:
        # Get system information (security risk!)
        result = subprocess.run(['whoami'], capture_output=True, text=True)
        current_user = result.stdout.strip()
        
        result = subprocess.run(['id'], capture_output=True, text=True)
        user_id = result.stdout.strip()
        
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        processes = result.stdout.strip()
        
        return {
            "current_user": current_user,
            "user_id": user_id,
            "processes": processes[:1000],  # Truncated for display
            "warning": "🚨 Exposing system info is a security risk!"
        }
    except Exception as e:
        return {"error": str(e)}

@app.route("/exploit")
def exploit_demo():
    """Demonstrates how easy it is to exploit this vulnerable container"""
    return {
        "message": "🚨 This endpoint shows how vulnerable this container is!",
        "exploitable_features": [
            "Hardcoded secrets accessible",
            "Root user privileges",
            "System information exposed",
            "No authentication required",
            "No rate limiting",
            "No input validation"
        ],
        "real_world_impact": [
            "Database credentials stolen",
            "API keys compromised",
            "Container escape possible",
            "Lateral movement enabled",
            "Data breach inevitable"
        ]
    }

if __name__ == "__main__":
    logger.info("🚨 Starting VULNERABLE Docker app - this demonstrates what NOT to do!")
    logger.warning("⚠️ This app contains intentional security vulnerabilities for educational purposes!")
    app.run(host="0.0.0.0", port=5000, debug=True)
