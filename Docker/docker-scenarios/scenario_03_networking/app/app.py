from flask import Flask, render_template_string, request
import redis
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Initialize Redis connection with error handling
try:
    logger.info(f"Attempting to connect to Redis at {REDIS_HOST}:6379")
    r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    # Test the connection
    r.ping()
    redis_available = True
    logger.info("✅ Redis connection successful!")
except (redis.ConnectionError, redis.RedisError) as e:
    redis_available = False
    logger.error(f"❌ Redis connection failed: {e}")

TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>🏆 Docker Voting App</title>
    <style>
        body {
            background: linear-gradient(135deg, #f8ffae 0%, #43c6ac 100%);
            font-family: 'Segoe UI', 'Arial', sans-serif;
            text-align: center;
            padding: 0;
            margin: 0;
            min-height: 100vh;
        }
        .container {
            margin-top: 60px;
            background: rgba(255,255,255,0.9);
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31,38,135,0.2);
            display: inline-block;
            padding: 40px 60px 30px 60px;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 0.2em;
            color: #2d3a4b;
        }
        h2 {
            color: #43c6ac;
            margin-bottom: 1.5em;
        }
        .vote-btn {
            font-size: 1.5em;
            padding: 20px 40px;
            margin: 20px 30px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: background 0.2s, transform 0.2s;
            box-shadow: 0 2px 8px rgba(67,198,172,0.15);
        }
        .vote-btn.wfh {
            background: linear-gradient(90deg, #f7971e 0%, #ffd200 100%);
            color: #2d3a4b;
        }
        .vote-btn.wfh:hover {
            background: linear-gradient(90deg, #ffd200 0%, #f7971e 100%);
            transform: scale(1.07);
        }
        .vote-btn.wfo {
            background: linear-gradient(90deg, #43c6ac 0%, #191654 100%);
            color: #fff;
        }
        .vote-btn.wfo:hover {
            background: linear-gradient(90deg, #191654 0%, #43c6ac 100%);
            transform: scale(1.07);
        }
        .votes {
            margin-top: 30px;
            display: flex;
            justify-content: center;
            gap: 60px;
        }
        .vote-box {
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(67,198,172,0.10);
            padding: 30px 40px;
            min-width: 160px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .vote-label {
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        .vote-count {
            font-size: 2.5em;
            font-weight: bold;
            color: #43c6ac;
        }
        .emoji {
            font-size: 2.2em;
            margin-bottom: 10px;
        }
        .footer {
            margin-top: 50px;
            color: #2d3a4b;
            font-size: 1.1em;
            opacity: 0.7;
        }
        .error-message {
            background: #ff6b6b;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1.1em;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-online {
            background: #4CAF50;
        }
        .status-offline {
            background: #f44336;
        }
        .success-message {
            background: #4CAF50;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1.1em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 Docker Voting App</h1>
        <h2>Which do you prefer?</h2>
        
        {% if show_error %}
        <div class="error-message">
            <span class="status-indicator status-offline"></span>
            <strong>Voting Failed!</strong><br>
            Cannot connect to Redis at {{ redis_host }}:6379<br>
            This demonstrates what happens when containers can't communicate!
        </div>
        {% elif vote_success %}
        <div class="success-message">
            <span class="status-indicator status-online"></span>
            <strong>Vote Recorded Successfully!</strong><br>
            Your vote was saved to Redis at {{ redis_host }}:6379
        </div>
        {% elif redis_available %}
        <div class="success-message">
            <span class="status-indicator status-online"></span>
            <strong>Database Connected</strong> - Redis is available at {{ redis_host }}:6379
        </div>
        {% endif %}
        
        <form method="POST">
            <button class="vote-btn wfh" name="vote" value="wfh">🏡 WFH (Work From Home)</button>
            <button class="vote-btn wfo" name="vote" value="wfo">🏢 WFO (Work From Office)</button>
        </form>
        <div class="votes">
            <div class="vote-box">
                <div class="emoji">🏡</div>
                <div class="vote-label">WFH Votes</div>
                <div class="vote-count">{{ wfh }}</div>
            </div>
            <div class="vote-box">
                <div class="emoji">🏢</div>
                <div class="vote-label">WFO Votes</div>
                <div class="vote-count">{{ wfo }}</div>
            </div>
        </div>
    </div>
    <div class="footer">
        Made with ❤️ for Today's Workshop for you!
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    wfh = 0
    wfo = 0
    show_error = False
    vote_success = False
    
    if request.method == "POST":
        logger.info("User attempted to vote")
        # User tried to vote - check if Redis is available
        if not redis_available:
            logger.error("Voting failed - Redis not available")
            show_error = True
        else:
            try:
                vote = request.form["vote"]
                logger.info(f"Recording vote for: {vote}")
                r.incr(f"votes:{vote}")
                logger.info(f"Vote recorded successfully for: {vote}")
                vote_success = True
            except (redis.ConnectionError, redis.RedisError) as e:
                logger.error(f"Redis error during voting: {e}")
                show_error = True
    
    if redis_available and not show_error:
        try:
            logger.info("Reading vote counts from Redis")
            wfh = r.get("votes:wfh") or 0
            wfo = r.get("votes:wfo") or 0
            logger.info(f"Vote counts - WFH: {wfh}, WFO: {wfo}")
        except (redis.ConnectionError, redis.RedisError) as e:
            logger.error(f"Redis error when reading votes: {e}")
            # Redis connection failed when reading votes
            pass
    
    return render_template_string(TEMPLATE, wfh=wfh, wfo=wfo, redis_available=redis_available, redis_host=REDIS_HOST, show_error=show_error, vote_success=vote_success)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 