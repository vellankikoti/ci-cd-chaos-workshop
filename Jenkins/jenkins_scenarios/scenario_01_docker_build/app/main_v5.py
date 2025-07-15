# app/main_v5.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import time
import random
import logging

app = FastAPI()

# Set up logging
logger = logging.getLogger("uvicorn.error")

@app.get("/", response_class=HTMLResponse)
def read_root():
    chaos_mode = random.choice(["delay", "error", "success"])
    
    if chaos_mode == "delay":
        delay_time = random.randint(3, 6)
        logger.warning(f"⚠️ Chaos mode: DELAYING for {delay_time} seconds...")
        time.sleep(delay_time)
        html = f"""
        <html>
          <body style="text-align: center; font-family: sans-serif; color: orange;">
            <h1>⚠️ Delayed Response!</h1>
            <p>This request was delayed by {delay_time} seconds due to chaos engineering.</p>
          </body>
        </html>
        """
        return html

    elif chaos_mode == "error":
        logger.error("💥 Chaos mode: CRASH triggered!")
        html = """
        <html>
          <body style="text-align: center; font-family: sans-serif; color: red;">
            <h1>💥 Chaos unleashed!</h1>
            <p>This version intentionally fails to simulate chaos in production!</p>
            <p>🚨 Remember: Good CI/CD pipelines save you from disasters like this!</p>
          </body>
        </html>
        """
        # Raise an exception that FastAPI will render as a 500 error
        raise Exception(html)

    else:
        logger.info("✅ Chaos mode: SUCCESS!")
        emojis = "🐍" * 5
        html = f"""
        <html>
          <body style="text-align: center; font-family: sans-serif; color: green;">
            <h1>{emojis} Hello from Version 5 of the CI/CD Chaos Workshop!</h1>
            <p>🎉 Congratulations, this request survived the chaos!</p>
            {"".join(
                f'<img src="https://www.python.org/static/community_logos/python-logo.png" width="80"/>' 
                for _ in range(5)
            )}
          </body>
        </html>
        """
        return html


@app.get("/version")
def get_version():
    return {"version": "v5"}

@app.get("/health")
def health():
    return {"status": "healthy"}
