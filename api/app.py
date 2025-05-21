from flask import Flask, render_template, request, redirect, url_for, g, flash, abort, jsonify, send_file, Response, make_response
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.config['SECRET_KEY'] = "gCKAJoHvT1"
app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_HTTPONLY=True,
  SESSION_COOKIE_SAMESITE='Lax',
)

@app.route("/", methods=["GET"])
def main():
    accept_header = request.headers.get('Accept', '')

    if 'text/plain' in accept_header:
        with open("api/loader.lua", 'r') as f:
            content = f.read()
        return Response(content, content_type='text/plain')

    return render_template("redirect.html")
