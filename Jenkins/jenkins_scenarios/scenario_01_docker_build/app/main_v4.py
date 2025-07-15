# app/main_v4.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    version = 4
    emojis = "🐍" * version
    message = f"{emojis} Hello from Version {version} of the CI/CD Chaos Workshop!"
    images = "".join(
        f'<img src="https://www.python.org/static/community_logos/python-logo.png" width="100"/>' 
        for _ in range(version)
    )
    html = f"""
    <html>
      <body style="text-align: center; font-family: sans-serif;">
        <h1>{message}</h1>
        {images}
      </body>
    </html>
    """
    return html

@app.get("/version")
def get_version():
    return {"version": f"v{version}"}

@app.get("/health")
def health():
    return {"status": "healthy"}
