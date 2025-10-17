#!/usr/bin/env python3
"""
Simple Voting App - WFH vs WFO
Stores votes in Redis - Simple and works!

This is the hero solution version of the voting app for Kubernetes deployment demo.
For the basic version, see simple-voting-app/vote-app.py
"""
from flask import Flask, render_template_string, request, jsonify
import redis
import os
import json

app = Flask(__name__)

# Connect to Redis with retry
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))

def connect_to_redis(max_retries=30):
    """Connect to Redis with retries"""
    import time
    for i in range(max_retries):
        try:
            r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
            r.ping()
            print(f"✅ Connected to Redis at {redis_host}:{redis_port}")
            return r
        except redis.exceptions.ConnectionError:
            print(f"⏳ Waiting for Redis... (attempt {i+1}/{max_retries})")
            time.sleep(2)
    raise Exception("Could not connect to Redis after multiple attempts")

r = connect_to_redis()

# Initialize vote counts if not exists
if not r.exists('votes'):
    r.set('votes', json.dumps({'WFH': 0, 'WFO': 0}))

VOTE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vote: WFH vs WFO</title>
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
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: fadeIn 0.5s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }
        .vote-buttons {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }
        .vote-btn {
            flex: 1;
            padding: 60px 20px;
            border: none;
            border-radius: 15px;
            font-size: 2em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .wfh {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .wfo {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .vote-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        .vote-btn:active {
            transform: translateY(-2px);
        }
        .emoji {
            display: block;
            font-size: 3em;
            margin-bottom: 10px;
        }
        .message {
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 1.2em;
            font-weight: bold;
            display: none;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
        }
        .info {
            text-align: center;
            color: #666;
            margin-top: 20px;
            font-size: 0.9em;
        }
        .current-votes {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .vote-count {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            font-size: 1.1em;
        }
        .count {
            font-weight: bold;
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗳️ Vote Now!</h1>
        <p class="subtitle">Work From Home vs Work From Office</p>

        <div class="vote-buttons">
            <button class="vote-btn wfh" onclick="vote('WFH')">
                <span class="emoji">🏠</span>
                <div>WFH</div>
            </button>
            <button class="vote-btn wfo" onclick="vote('WFO')">
                <span class="emoji">🏢</span>
                <div>WFO</div>
            </button>
        </div>

        <div id="message" class="message"></div>

        <div class="current-votes">
            <h3 style="text-align: center; margin-bottom: 15px; color: #333;">Current Results</h3>
            <div class="vote-count">
                <span>🏠 Work From Home:</span>
                <span class="count" id="wfh-count">0</span>
            </div>
            <div class="vote-count">
                <span>🏢 Work From Office:</span>
                <span class="count" id="wfo-count">0</span>
            </div>
        </div>

        <div class="info">
            Vote for your preference! Results update in real-time.
        </div>
    </div>

    <script>
        function vote(option) {
            fetch('/vote', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({option: option})
            })
            .then(response => response.json())
            .then(data => {
                const msg = document.getElementById('message');
                msg.textContent = '✅ Vote recorded for ' + option + '!';
                msg.className = 'message success';
                msg.style.display = 'block';

                // Update counts
                updateCounts();

                setTimeout(() => {
                    msg.style.display = 'none';
                }, 3000);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }

        function updateCounts() {
            fetch('/results')
            .then(response => response.json())
            .then(data => {
                document.getElementById('wfh-count').textContent = data.WFH;
                document.getElementById('wfo-count').textContent = data.WFO;
            });
        }

        // Update counts every 2 seconds
        setInterval(updateCounts, 2000);

        // Initial load
        updateCounts();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(VOTE_TEMPLATE)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    option = data.get('option')

    if option not in ['WFH', 'WFO']:
        return jsonify({'error': 'Invalid option'}), 400

    # Get current votes
    votes = json.loads(r.get('votes'))

    # Increment vote
    votes[option] += 1

    # Save back to Redis
    r.set('votes', json.dumps(votes))

    print(f"Vote recorded: {option}. Current: WFH={votes['WFH']}, WFO={votes['WFO']}")

    return jsonify({'success': True, 'votes': votes})

@app.route('/results')
def results():
    votes = json.loads(r.get('votes'))
    return jsonify(votes)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("Starting Voting App...")
    print(f"Redis: {redis_host}:{redis_port}")
    app.run(host='0.0.0.0', port=8080, debug=True)
