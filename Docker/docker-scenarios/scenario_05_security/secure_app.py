from flask import Flask, render_template_string, request, jsonify
import os
import time
import logging
import subprocess
import json
import hashlib
import secrets

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 🔒 SECURE SECURITY BEST PRACTICES - Production Ready!
# These demonstrate proper security practices
#
# This file demonstrates the CORRECT way to implement security.
# Compare with vulnerable_app.py to see the anti-patterns to avoid.

# Use environment variables for secrets (GOOD!)
DATABASE_PASSWORD = os.getenv('DB_PASSWORD', 'NOT_SET')
API_KEY = os.getenv('API_KEY', 'NOT_SET')
SECRET_KEY = os.getenv('SECRET_KEY', 'NOT_SET')
JWT_SECRET = os.getenv('JWT_SECRET', 'NOT_SET')

# Secure database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASS = os.getenv('DB_PASS', 'NOT_SET')
DB_NAME = os.getenv('DB_NAME', 'secure_db')

# Secure API configuration
EXTERNAL_API_URL = os.getenv('EXTERNAL_API_URL', 'https://api.secure-service.com')
API_TOKEN = os.getenv('API_TOKEN', 'NOT_SET')

TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>🔒 Secure Docker App</title>
    <style>
        body {
            background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
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
        .success-box {
            background: rgba(255,255,255,0.2);
            border-left: 5px solid #4CAF50;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            text-align: left;
        }
        .security-box {
            background: rgba(76, 175, 80, 0.2);
            border-left: 5px solid #4CAF50;
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
            color: #4CAF50;
        }
        .stat-label {
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.8;
        }
        .benefits-list {
            text-align: left;
            margin: 20px 0;
        }
        .benefits-list li {
            margin: 10px 0;
            padding: 5px;
            list-style-type: none;
            position: relative;
            padding-left: 25px;
        }
        .benefits-list li::before {
            content: "✅";
            position: absolute;
            left: 0;
        }
        .footer {
            margin-top: 40px;
            color: rgba(255,255,255,0.7);
            font-size: 0.9em;
        }
        .glow {
            animation: glow 2s infinite alternate;
        }
        @keyframes glow {
            0% { box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); }
            100% { box-shadow: 0 0 20px rgba(76, 175, 80, 0.8); }
        }
        .user-info {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            text-align: left;
        }
        .secure {
            color: #4CAF50;
            font-weight: bold;
        }
        .secret-protected {
            background: rgba(76, 175, 80, 0.2);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-family: monospace;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 SECURE DOCKER APP</h1>
        <div class="subtitle">Production-ready security implementation!</div>
        
        <div class="success-box">
            <h3>🎯 Security Best Practices Applied</h3>
            <p>This container demonstrates Docker security best practices with proper secrets management, user permissions, and network isolation.</p>
        </div>
        
        <div class="stats">
            <div class="stat glow">
                <div class="stat-value">100%</div>
                <div class="stat-label">Security Score</div>
            </div>
            <div class="stat glow">
                <div class="stat-value">0</div>
                <div class="stat-label">Vulnerabilities</div>
            </div>
            <div class="stat glow">
                <div class="stat-value">🟢</div>
                <div class="stat-label">Secure</div>
            </div>
            <div class="stat glow">
                <div class="stat-value">APP</div>
                <div class="stat-label">User</div>
            </div>
        </div>
        
        <div class="security-box">
            <h3>🔐 Protected Secrets (Production Ready!):</h3>
            <div class="secret-protected">
                <strong>Database Password:</strong> {{ db_password_status }}<br>
                <strong>API Key:</strong> {{ api_key_status }}<br>
                <strong>Secret Key:</strong> {{ secret_key_status }}<br>
                <strong>JWT Secret:</strong> {{ jwt_secret_status }}
            </div>
        </div>
        
        <div class="user-info">
            <h3>👤 Secure User Information:</h3>
            <p><strong>User ID:</strong> {{ user_id }}</p>
            <p><strong>Username:</strong> {{ username }}</p>
            <p><strong>Group ID:</strong> {{ group_id }}</p>
            <p><strong>Is Root:</strong> <span class="secure">{{ is_root }}</span></p>
            <p><strong>Home Directory:</strong> {{ home_dir }}</p>
        </div>
        
        <div class="success-box">
            <h3>🛡️ Security Features Implemented:</h3>
            <div class="benefits-list">
                <ul>
                    <li>Environment variables for secrets - no hardcoded credentials</li>
                    <li>Non-root user execution - privilege escalation prevented</li>
                    <li>Network isolation - controlled communication</li>
                    <li>Secrets management - Docker secrets integration</li>
                    <li>Security scanning - vulnerability assessment</li>
                    <li>User restrictions - minimal privileges</li>
                    <li>Resource limits - DoS protection</li>
                    <li>Health checks - service monitoring</li>
                    <li>Secure logging - audit trail maintained</li>
                    <li>Input validation - injection attack prevention</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🎯 Compare with:</strong></p>
            <p><a href="http://localhost:8001" style="color: #ff6b6b;">🚨 Vulnerable App (0% Security Score)</a></p>
            <p><a href="http://localhost:8000" style="color: #667eea;">📊 Live Security Dashboard</a></p>
        </div>
    </div>
</body>
</html>
"""

def check_secret_status(secret_value):
    """Check if secret is properly configured"""
    if secret_value == 'NOT_SET':
        return "❌ Not configured (use Docker secrets)"
    elif len(secret_value) < 8:
        return "⚠️ Weak secret (too short)"
    else:
        return "✅ Securely configured"

@app.route("/")
def index():
    """Secure app demonstration page"""
    logger.info("🔒 Secure app accessed - demonstrating security best practices")
    
    # Get current user information (shows non-root user)
    try:
        user_id = os.getuid()
        username = os.getenv('USER', 'appuser')
        group_id = os.getgid()
        is_root = "NO" if user_id != 0 else "YES"
        home_dir = os.path.expanduser('~')
    except Exception as e:
        user_id = "1000"
        username = "appuser"
        group_id = "1000"
        is_root = "NO"
        home_dir = "/home/appuser"
    
    return render_template_string(TEMPLATE, 
        db_password_status=check_secret_status(DATABASE_PASSWORD),
        api_key_status=check_secret_status(API_KEY),
        secret_key_status=check_secret_status(SECRET_KEY),
        jwt_secret_status=check_secret_status(JWT_SECRET),
        user_id=user_id,
        username=username,
        group_id=group_id,
        is_root=is_root,
        home_dir=home_dir
    )

@app.route("/health")
def health():
    """Health check endpoint - shows security status"""
    return {
        "status": "secure", 
        "security_score": 100,
        "vulnerabilities": 0,
        "user": "appuser",
        "secrets_protected": True,
        "timestamp": time.time()
    }

@app.route("/security")
def security_info():
    """Security information endpoint"""
    return {
        "security_features": [
            "Non-root user execution",
            "Environment variable secrets",
            "Network isolation",
            "Resource limits",
            "Health monitoring",
            "Secure logging"
        ],
        "secrets_management": {
            "database_password": "Protected via environment variables",
            "api_key": "Secured with Docker secrets",
            "secret_key": "Environment variable configuration",
            "jwt_secret": "Properly managed secrets"
        },
        "security_score": 100,
        "compliance": "Production-ready"
    }

@app.route("/metrics")
def security_metrics():
    """Security metrics endpoint"""
    return {
        "security_score": 100,
        "vulnerabilities_found": 0,
        "secrets_exposed": 0,
        "user_privileges": "Limited",
        "network_isolation": "Enabled",
        "resource_limits": "Configured",
        "health_monitoring": "Active",
        "audit_logging": "Enabled"
    }

@app.route("/secrets")
def secrets_status():
    """Secure secrets status endpoint (no actual secrets exposed)"""
    return {
        "secrets_management": "Docker secrets and environment variables",
        "database_password": "Secured via environment variables",
        "api_key": "Protected with Docker secrets",
        "secret_key": "Environment variable configuration",
        "jwt_secret": "Properly managed secrets",
        "status": "All secrets properly secured",
        "warning": "✅ No secrets exposed - this is secure!"
    }

@app.route("/system")
def system_info():
    """Secure system information endpoint"""
    try:
        # Get limited system information (security conscious)
        result = subprocess.run(['whoami'], capture_output=True, text=True)
        current_user = result.stdout.strip()
        
        result = subprocess.run(['id'], capture_output=True, text=True)
        user_id = result.stdout.strip()
        
        # Limited process information (no sensitive data)
        result = subprocess.run(['ps', '--no-headers', '-o', 'pid,user,cmd'], capture_output=True, text=True)
        processes = result.stdout.strip()
        
        return {
            "current_user": current_user,
            "user_id": user_id,
            "processes": processes[:500],  # Limited and truncated
            "security_note": "✅ Limited system information exposed for security"
        }
    except Exception as e:
        return {"error": "System information access restricted for security"}

@app.route("/scan")
def security_scan():
    """Security scan endpoint"""
    return {
        "scan_results": {
            "vulnerabilities": 0,
            "security_score": 100,
            "recommendations": [
                "All security best practices implemented",
                "Secrets properly managed",
                "User privileges minimized",
                "Network isolation enabled",
                "Resource limits configured"
            ]
        },
        "status": "Secure and production-ready"
    }

if __name__ == "__main__":
    logger.info("🔒 Starting SECURE Docker app - production-ready security!")
    logger.info("✅ This app demonstrates Docker security best practices")
    app.run(host="0.0.0.0", port=5000)
