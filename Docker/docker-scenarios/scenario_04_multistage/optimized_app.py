from flask import Flask, render_template_string, jsonify
import time
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ✨ OPTIMIZED MULTI-STAGE DOCKER BEST PRACTICES - Production Ready!
# This file demonstrates the CORRECT way to implement multi-stage builds.
# Compare with bloated_app.py to see the anti-patterns to avoid.

TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>✨ Optimized Multi-Stage App</title>
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
        .success-box {
            background: rgba(255,255,255,0.2);
            border-left: 5px solid #4CAF50;
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
        .multi-stage-info {
            background: rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: left;
        }
        .stage {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        .stage h4 {
            margin: 0 0 10px 0;
            color: #4CAF50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✨ OPTIMIZED MULTI-STAGE APP</h1>
        <div class="subtitle">Production-ready Docker optimization!</div>
        
        <div class="success-box">
            <h3>🎯 Multi-Stage Build Success</h3>
            <p>This container demonstrates Docker best practices using multi-stage builds for optimal size, security, and performance.</p>
        </div>
        
        <div class="stats">
            <div class="stat glow">
                <div class="stat-value">267MB</div>
                <div class="stat-label">Image Size</div>
            </div>
            <div class="stat glow">
                <div class="stat-value">8</div>
                <div class="stat-label">Layers</div>
            </div>
            <div class="stat glow">
                <div class="stat-value">✅</div>
                <div class="stat-label">Security</div>
            </div>
            <div class="stat glow">
                <div class="stat-value">FAST</div>
                <div class="stat-label">Performance</div>
            </div>
        </div>
        
        <div class="multi-stage-info">
            <h3>🏗️ Multi-Stage Build Process:</h3>
            <div class="stage">
                <h4>Stage 1: Builder</h4>
                <p>• Installs build tools (gcc, build-essential)<br>
                • Creates virtual environment<br>
                • Installs Python dependencies<br>
                • Heavy but discarded after build</p>
            </div>
            <div class="stage">
                <h4>Stage 2: Production</h4>
                <p>• Minimal base image (python:slim)<br>
                • Only runtime dependencies<br>
                • Non-root user for security<br>
                • Optimized for deployment</p>
            </div>
        </div>
        
        <div class="success-box">
            <h3>🚀 Benefits of this approach:</h3>
            <div class="benefits-list">
                <ul>
                    <li>94% size reduction (4.2GB → 267MB)</li>
                    <li>Minimal attack surface - only necessary packages</li>
                    <li>Production optimized - no development tools</li>
                    <li>Fast deployments - smaller image transfers</li>
                    <li>Security hardened - non-root user</li>
                    <li>Layer caching optimized</li>
                    <li>Health checks included</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🎯 Compare with:</strong></p>
            <p><a href="http://localhost:8001" style="color: #ff6b6b;">🚨 Bloated App (4.2GB)</a></p>
            <p><a href="http://localhost:8000" style="color: #667eea;">📊 Live Comparison Dashboard</a></p>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    """Optimized app demonstration page"""
    logger.info("Optimized multi-stage app accessed - demonstrating best practices")
    return render_template_string(TEMPLATE)

@app.route("/health")
def health():
    """Health check endpoint for Docker health check"""
    return jsonify({
        "status": "healthy", 
        "type": "optimized", 
        "size": "267MB",
        "user": os.getenv("USER", "appuser"),
        "timestamp": time.time()
    }), 200

if __name__ == "__main__":
    logger.info("✨ Starting OPTIMIZED multi-stage Docker app - production ready!")
    app.run(host="0.0.0.0", port=5000)