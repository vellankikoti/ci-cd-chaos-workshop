from flask import Flask, render_template_string, request, jsonify
import os
import time
import logging
import subprocess
import json
import random
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 🚨 FRAGILE RESILIENCE ANTI-PATTERNS - DO NOT USE IN PRODUCTION!
# These are intentionally fragile for educational purposes
# 
# This file demonstrates what NOT to do in production.
# Compare with resilient_app.py to see the proper implementation.

# Global variables to simulate fragility
failure_count = 0
last_failure = None
memory_usage = 0
cpu_usage = 0

TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>💥 Fragile Docker App</title>
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
        .fragility-list {
            text-align: left;
            margin: 20px 0;
        }
        .fragility-list li {
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
        .failure-indicator {
            background: rgba(255,0,0,0.2);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-family: monospace;
            word-break: break-all;
        }
        .resource-info {
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
        .test-button {
            background: #ff6b6b;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1em;
            margin: 10px;
            transition: background 0.3s;
        }
        .test-button:hover {
            background: #ff5252;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💥 FRAGILE DOCKER APP</h1>
        <div class="subtitle">This is what NOT to do in production!</div>
        
        <div class="danger-box">
            <h3>⚠️ CRITICAL RESILIENCE WARNING</h3>
            <p>This container demonstrates common Docker resilience mistakes that lead to constant failures and poor user experience.</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value pulse">0%</div>
                <div class="stat-label">Uptime</div>
            </div>
            <div class="stat">
                <div class="stat-value pulse">{{ failure_count }}</div>
                <div class="stat-label">Failures</div>
            </div>
            <div class="stat">
                <div class="stat-value pulse">🔴</div>
                <div class="stat-label">Status</div>
            </div>
            <div class="stat">
                <div class="stat-value pulse">NONE</div>
                <div class="stat-label">Recovery</div>
            </div>
        </div>
        
        <div class="warning-box">
            <h3>💥 Current Failure Status:</h3>
            <div class="failure-indicator">
                <strong>Failure Count:</strong> {{ failure_count }}<br>
                <strong>Last Failure:</strong> {{ last_failure }}<br>
                <strong>Memory Usage:</strong> {{ memory_usage }}%<br>
                <strong>CPU Usage:</strong> {{ cpu_usage }}%
            </div>
        </div>
        
        <div class="resource-info">
            <h3>📊 Resource Usage (No Limits!):</h3>
            <p><strong>Memory:</strong> <span class="danger">{{ memory_usage }}% (No limits - will crash!)</span></p>
            <p><strong>CPU:</strong> <span class="danger">{{ cpu_usage }}% (No throttling - will freeze!)</span></p>
            <p><strong>Health Check:</strong> <span class="danger">None (No monitoring!)</span></p>
            <p><strong>Restart Policy:</strong> <span class="danger">No (Manual intervention required!)</span></p>
        </div>
        
        <div class="warning-box">
            <h3>🐛 Critical Resilience Problems:</h3>
            <div class="fragility-list">
                <ul>
                    <li>🔴 No health checks - no failure detection</li>
                    <li>🔴 No restart policies - manual recovery required</li>
                    <li>🔴 No resource limits - memory/CPU exhaustion</li>
                    <li>🔴 No graceful shutdown - abrupt failures</li>
                    <li>🔴 No monitoring - blind to problems</li>
                    <li>🔴 No error handling - crashes propagate</li>
                    <li>🔴 No circuit breakers - cascade failures</li>
                    <li>🔴 No load balancing - single point of failure</li>
                    <li>🔴 No backup strategies - data loss risk</li>
                    <li>🔴 No rollback mechanisms - stuck in bad state</li>
                </ul>
            </div>
        </div>
        
        <div style="margin: 30px 0;">
            <button class="test-button" onclick="simulateFailure()">💥 Simulate Failure</button>
            <button class="test-button" onclick="consumeMemory()">🧠 Consume Memory</button>
            <button class="test-button" onclick="crashApp()">💀 Crash App</button>
        </div>
        
        <div class="footer">
            <p><strong>🎯 Compare with:</strong></p>
            <p><a href="http://localhost:8002" style="color: #4ecdc4;">🛡️ Resilient App (100% Uptime)</a></p>
            <p><a href="http://localhost:8000" style="color: #667eea;">📊 Live Resilience Dashboard</a></p>
        </div>
    </div>
    
    <script>
        function simulateFailure() {
            fetch('/simulate-failure', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    alert('💥 Failure simulated! ' + data.message);
                    location.reload();
                });
        }
        
        function consumeMemory() {
            fetch('/consume-memory', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    alert('🧠 Memory consumed! ' + data.message);
                    location.reload();
                });
        }
        
        function crashApp() {
            fetch('/crash', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    alert('💀 App crashed! ' + data.message);
                });
        }
    </script>
</body>
</html>
"""

def simulate_resource_usage():
    """Simulate resource consumption to show fragility"""
    global memory_usage, cpu_usage
    while True:
        # Simulate increasing resource usage
        memory_usage = min(95, memory_usage + random.randint(1, 5))
        cpu_usage = min(100, cpu_usage + random.randint(1, 3))
        time.sleep(2)

# Start resource simulation in background
resource_thread = threading.Thread(target=simulate_resource_usage, daemon=True)
resource_thread.start()

@app.route("/")
def index():
    """Fragile app demonstration page"""
    logger.info("💥 Fragile app accessed - demonstrating resilience anti-patterns")
    
    return render_template_string(TEMPLATE, 
        failure_count=failure_count,
        last_failure=last_failure or "None yet",
        memory_usage=memory_usage,
        cpu_usage=cpu_usage
    )

@app.route("/health")
def health():
    """Health check endpoint - shows fragility issues"""
    return {
        "status": "fragile", 
        "uptime": 0,
        "failures": failure_count,
        "memory_usage": memory_usage,
        "cpu_usage": cpu_usage,
        "health_check": "None",
        "restart_policy": "None",
        "timestamp": time.time()
    }

@app.route("/simulate-failure", methods=["POST"])
def simulate_failure():
    """Simulate a failure to demonstrate fragility"""
    global failure_count, last_failure
    
    failure_count += 1
    last_failure = time.strftime("%H:%M:%S")
    
    logger.warning(f"💥 Simulated failure #{failure_count}")
    
    return {
        "message": f"Failure #{failure_count} simulated at {last_failure}",
        "failure_count": failure_count,
        "status": "fragile"
    }

@app.route("/consume-memory", methods=["POST"])
def consume_memory():
    """Simulate memory consumption"""
    global memory_usage
    
    memory_usage = min(95, memory_usage + 20)
    
    logger.warning(f"🧠 Memory consumption increased to {memory_usage}%")
    
    return {
        "message": f"Memory consumption increased to {memory_usage}%",
        "memory_usage": memory_usage,
        "status": "dangerous"
    }

@app.route("/crash", methods=["POST"])
def crash_app():
    """Simulate app crash"""
    logger.error("💀 App crash simulated!")
    
    # Simulate crash by exiting
    return {
        "message": "App crashed! No restart policy - manual intervention required!",
        "status": "crashed"
    }

@app.route("/metrics")
def metrics():
    """Metrics endpoint showing fragility"""
    return {
        "uptime_percentage": 0,
        "failure_rate": failure_count,
        "memory_usage": memory_usage,
        "cpu_usage": cpu_usage,
        "health_checks": 0,
        "auto_restarts": 0,
        "resilience_score": 0
    }

if __name__ == "__main__":
    logger.info("💥 Starting FRAGILE Docker app - this demonstrates what NOT to do!")
    logger.warning("⚠️ This app contains intentional fragility for educational purposes!")
    app.run(host="0.0.0.0", port=5000, debug=True)
