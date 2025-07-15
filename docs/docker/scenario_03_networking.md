# 🚀 Scenario 03 — Docker Networking Magic

## 🎯 Scenario Goal

Demonstrate **real-world Docker networking problems** and how to fix them by:

✅ Running a Python Flask **Voting App** (WFO vs WFH)  
✅ Letting workshop attendees vote live via a public URL (ngrok or Cloudflare Tunnel)  
✅ Simulating networking failures:
- Missing database
- Containers in separate networks
✅ Fixing networking issues → **everything magically works!**

This scenario creates an unforgettable **AHA moment** for learners.

---

# ✅ Directory Structure

```
scenario_03_networking/
│
├── app/
│     ├── app.py              # Enhanced Flask app with error handling & beautiful UI
│     ├── requirements.txt
│     └── Dockerfile
├── scripts/
│     ├── cleanup.sh
│     ├── fix_network.sh
│     ├── expose_ngrok.sh
│     ├── expose_cloudflared.sh
│     └── [other utility scripts]
├── demo_simple.sh            # Automated 4-step demo
├── demo_manual.sh            # Interactive demo with explanations
└── README.md
```

---

# ✅ How The Voting App Works

## Enhanced Flask Voting App

**Beautiful UI with real-time status indicators:**

- ✅ Vote **WFH** (Work From Home) - 🏡
- ✅ Vote **WFO** (Work From Office) - 🏢
- ✅ Real-time Redis connectivity status
- ✅ Success/error messages for educational clarity
- ✅ Vote counts stored in Redis under keys:
  - `votes:wfh`
  - `votes:wfo`

✅ Total votes shown live with beautiful styling.

---

## app/app.py (Enhanced Version)

```python
from flask import Flask, render_template_string, request
import redis
import os
import logging

# Set up logging for debugging
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

# Beautiful HTML template with status indicators
TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>🏆 Docker Voting App</title>
    <style>
        /* Beautiful gradient background and modern styling */
        body {
            background: linear-gradient(135deg, #f8ffae 0%, #43c6ac 100%);
            font-family: 'Segoe UI', 'Arial', sans-serif;
            text-align: center;
            padding: 0;
            margin: 0;
            min-height: 100vh;
        }
        /* Container styling with glassmorphism effect */
        .container {
            margin-top: 60px;
            background: rgba(255,255,255,0.9);
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31,38,135,0.2);
            display: inline-block;
            padding: 40px 60px 30px 60px;
        }
        /* Status indicators for educational clarity */
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-online { background: #4CAF50; }
        .status-offline { background: #f44336; }
        
        /* Error and success messages */
        .error-message {
            background: #ff6b6b;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1.1em;
        }
        .success-message {
            background: #4CAF50;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1.1em;
        }
        
        /* Beautiful voting buttons */
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
        .vote-btn.wfo {
            background: linear-gradient(90deg, #43c6ac 0%, #191654 100%);
            color: #fff;
        }
        .vote-btn:hover {
            transform: scale(1.07);
        }
        
        /* Vote count display */
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
        .vote-count {
            font-size: 2.5em;
            font-weight: bold;
            color: #43c6ac;
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
```

---

## app/requirements.txt

```
flask
redis
```

---

## app/Dockerfile

```Dockerfile
FROM python:3.10

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

---

# ✅ Enhanced Demo Execution

## 🎯 **4-Step Educational Flow**

The demo now follows a clear, educational progression:

### **STEP 1: App Without Database (Expected Failure)**
- Build and run Flask app without Redis
- Demonstrate container isolation
- Show realistic error messages

### **STEP 2: Database in Wrong Network (Expected Failure)**  
- Add Redis but in separate network
- Demonstrate network isolation concepts
- Show hostname resolution failures

### **STEP 3: Fix the Network (Success!)**
- Create custom Docker network
- Place both containers in same network
- Demonstrate successful communication

### **STEP 4: Production-Ready Setup**
- Complete working microservices setup
- Real Redis connectivity and voting
- Network connectivity testing

---

# ✅ Running the Demo

## Automated Demo (Recommended)

```bash
# Run the complete 4-step demo automatically
./demo_simple.sh
```

**Features:**
- ✅ Automated testing of each step
- ✅ Real vote count validation
- ✅ Network connectivity verification
- ✅ Beautiful colored output
- ✅ Educational success/failure messages

## Interactive Demo

```bash
# Run with explanations and user interaction
./demo_manual.sh
```

**Features:**
- ✅ Step-by-step explanations
- ✅ User interaction prompts
- ✅ Educational commentary
- ✅ Manual verification steps

---

# ✅ Demo Scripts

## demo_simple.sh (Automated)

**Key Features:**
- ✅ **4 clear educational steps**
- ✅ **Real vote testing** with `awk` parsing
- ✅ **Network connectivity verification**
- ✅ **Beautiful colored output**
- ✅ **Comprehensive error handling**

**Sample Output:**
```
🚀 Docker Networking Magic - Automated Demo
========================================

🧹 Initial Cleanup
➤ Cleaning up containers and networks...
✅ Cleanup completed

🔴 STEP 1: App Without Database (Expected Failure)
➤ Building the Flask voting app...
✅ App built successfully
➤ Running app without Redis database...
✅ App container started
✅ App is accessible at http://localhost:5000
✅ Voting failed as expected - no database connection!

🔴 STEP 2: Database in Wrong Network (Expected Failure)
✅ Voting failed as expected - network isolation!

🟢 STEP 3: Fix the Network (Success!)
✅ Custom network 'vote-net' created
✅ Redis started in vote-net network
✅ App started in vote-net network
🎉 VOTING WORKS! The magic of Docker networking!
✅ Network connectivity: App can reach Redis on port 6379
✅ Redis connectivity: App can connect and ping Redis

🎉 Demo Complete!
✅ Container isolation and communication
✅ Docker network concepts
✅ How to fix common networking issues
✅ Real-world microservices patterns
```

## demo_manual.sh (Interactive)

**Key Features:**
- ✅ **Educational explanations** for each step
- ✅ **User interaction** with prompts
- ✅ **Manual verification** steps
- ✅ **Detailed commentary** on what's happening

---

# ✅ Making It Public

## Option 1 — Expose Via ngrok

```bash
# Install ngrok
brew install ngrok/ngrok/ngrok

# Expose the app
ngrok http 5000
```

✅ Share public URL like: `https://glorious-bear-1234.ngrok.io`

## Option 2 — Expose Via Cloudflare Tunnel

```bash
# Install cloudflared
brew install cloudflared

# Expose the app
cloudflared tunnel --url http://localhost:5000
```

✅ Get public URL like: `https://vote.mydomain.com`

---

# ✅ Clean Up

```bash
# Clean up all containers and networks
docker rm -f vote-app redis-server
docker network rm vote-net
```

Or use the cleanup script:

```bash
./scripts/cleanup.sh
```

---

# ✅ Key Improvements Made

## 🎯 **Educational Clarity**
- ✅ **4-step progression** instead of 8 confusing steps
- ✅ **Clear success/failure indicators**
- ✅ **Realistic error messages** only when voting fails
- ✅ **Beautiful UI** with status indicators

## 🔧 **Technical Enhancements**
- ✅ **Real Redis connectivity** testing
- ✅ **Proper vote count parsing** with `awk`
- ✅ **Network connectivity verification**
- ✅ **Comprehensive logging** for debugging
- ✅ **Robust error handling**

## 🚀 **Production-Ready Features**
- ✅ **Beautiful modern UI** with gradients
- ✅ **Real-time status indicators**
- ✅ **Educational success/error messages**
- ✅ **Comprehensive testing** of each step
- ✅ **Network connectivity validation**

---

# ✅ Learning Outcomes

## **What Attendees Learn:**
- ✅ **Container isolation** and communication
- ✅ **Docker network concepts** and troubleshooting
- ✅ **Real-world microservices** patterns
- ✅ **How to fix common** networking issues
- ✅ **Production-ready** application deployment

## **Key Takeaways:**
- ✅ Containers need explicit network configuration
- ✅ Custom networks enable service communication
- ✅ This pattern is used in production every day
- ✅ Docker networking is powerful but requires understanding

---

# ✅ Troubleshooting

## Common Issues:

**App not responding:**
```bash
# Check if containers are running
docker ps

# Check app logs
docker logs vote-app

# Check Redis logs
docker logs redis-server
```

**Voting not working:**
```bash
# Test Redis connectivity
docker exec vote-app python -c "import redis; r = redis.Redis(host='redis-server', port=6379); r.ping()"

# Check network connectivity
docker exec vote-app ping redis-server
```

**Network issues:**
```bash
# List networks
docker network ls

# Inspect network
docker network inspect vote-net
```

---

This enhanced scenario provides a **memorable learning experience** with real-world Docker networking challenges and solutions! 🚀