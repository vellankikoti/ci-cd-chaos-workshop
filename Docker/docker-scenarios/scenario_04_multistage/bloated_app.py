from flask import Flask, render_template_string
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 🚨 BLOATED DOCKER ANTI-PATTERNS - DO NOT USE IN PRODUCTION!
# This file demonstrates what NOT to do in production.
# Compare with optimized_app.py to see the proper multi-stage implementation.

TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>🚨 Bloated Docker App</title>
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
            max-width: 800px;
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
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
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
        .problems-list {
            text-align: left;
            margin: 20px 0;
        }
        .problems-list li {
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
    </style>
</head>
<body>
    <div class="container">
        <h1>🚨 BLOATED DOCKER APP</h1>
        <div class="subtitle">This is what NOT to do in production!</div>
        
        <div class="warning-box">
            <h3>⚠️ WARNING: Anti-Pattern Demo</h3>
            <p>This container demonstrates common Docker mistakes that lead to bloated, insecure, and slow deployments.</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value pulse">4.2GB</div>
                <div class="stat-label">Image Size</div>
            </div>
            <div class="stat">
                <div class="stat-value pulse">30+</div>
                <div class="stat-label">Layers</div>
            </div>
            <div class="stat">
                <div class="stat-value pulse">❌</div>
                <div class="stat-label">Security</div>
            </div>
            <div class="stat">
                <div class="stat-value pulse">SLOW</div>
                <div class="stat-label">Performance</div>
            </div>
        </div>
        
        <div class="warning-box">
            <h3>🐛 Problems with this approach:</h3>
            <div class="problems-list">
                <ul>
                    <li>🔴 Massive image size (4.2GB) - slow to deploy</li>
                    <li>🔴 Unnecessary packages - security vulnerabilities</li>
                    <li>🔴 Development tools in production - attack surface</li>
                    <li>🔴 No optimization - inefficient resource usage</li>
                    <li>🔴 Hardcoded secrets - security risk</li>
                    <li>🔴 No layer caching optimization</li>
                    <li>🔴 Root user - security vulnerability</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🎯 Compare with:</strong></p>
            <p><a href="http://localhost:8002" style="color: #4ecdc4;">✨ Optimized Multi-Stage App (267MB)</a></p>
            <p><a href="http://localhost:8000" style="color: #667eea;">📊 Live Comparison Dashboard</a></p>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    """Bloated app demonstration page"""
    logger.info("Bloated app accessed - demonstrating anti-patterns")
    return render_template_string(TEMPLATE)

@app.route("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "type": "bloated", "size": "4.2GB", "timestamp": time.time()}

if __name__ == "__main__":
    logger.info("🚨 Starting BLOATED Docker app - this demonstrates what NOT to do!")
    app.run(host="0.0.0.0", port=5000, debug=True)