from flask import Flask, render_template, request, redirect, url_for, g, flash, abort, jsonify, send_file, Response, make_response
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.config['SECRET_KEY'] = "gCKAJoHvT1"
app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_HTTPONLY=True,
  SESSION_COOKIE_SAMESITE='Lax',
)

@app.route('/', methods=["GET"])
def home():
  filePath = "api/loader.lua"
  file = open(filePath, 'r')
  fileRead = file.read()
  return render_template("main.html", fileRead=fileRead)
