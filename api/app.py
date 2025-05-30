from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, g, flash, abort, jsonify, send_file, Response, make_response
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
import base64
import time
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = "gCKAJoHvT1"
app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_HTTPONLY=True,
  SESSION_COOKIE_SAMESITE='Lax',
)

MongoConnection = MongoClient(
    "mongodb+srv://yvorexe:yvorbaog@yvorsite.krkrg.mongodb.net/?retryWrites=true&w=majority&appName=YvorSite",
    serverSelectionTimeoutMS=5000  # Set timeout to 5 seconds
)
Database = MongoConnection["ShardDB"]
Users = Database["Users"]

API_KEY = "xVn83p9aRzL7q2KfWu4TYjCbGdEX1oAa"

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-KEY') != API_KEY:
            return jsonify({"status": "error", "message": "Forbidden"}), 403
        return f(*args, **kwargs)
    return decorated_function

def IncrementExecute(new_values):
    username = str(new_values.get("1", "default_username"))[:100]
    profile_url = str(new_values.get("2", "default_profile_url"))[:200]
    hwid = str(new_values.get("3", "default_hwid"))[:100]
    
    try:
        user_id = int(new_values.get("4", 0))
    except (TypeError, ValueError):
        user_id = 0

    update_query = {
        "$inc": {"TotalExecutes.0": 1},
        "$set": {
            "TotalExecutes.1": username,
            "TotalExecutes.2": profile_url,
            "TotalExecutes.3": hwid,
            "TotalExecutes.4": user_id
        }
    }
    
    Users.update_one(
        {"_id": "683a0d4b79a633c096a0b4c4"},
        update_query,
        upsert=False
    )


@app.route("/", methods=["GET"])
def home():
    DATA = Users.find_one({"_id": "683a0d4b79a633c096a0b4c4"})
    
    EXEC = DATA["TotalExecutes"][0]
    RECENT = DATA["TotalExecutes"][1]
    PROFILE = DATA["TotalExecutes"][2]
    HWID = DATA["TotalExecutes"][3]
    ID = DATA["TotalExecutes"][4]
  
    if EXEC >= 1000:
        EXEC = f"{EXEC // 1000}k"
    else:
        EXEC = str(EXEC)
  
    return render_template("index.html", EXEC=EXEC, RECENT=RECENT, PROFILE=PROFILE, HWID=HWID, ID=ID)

@app.route("/api/users/v1/increment-execute", methods=["POST"])
@require_api_key
def api_execute():
    try:
        data = request.json
        new_values = data.get("new_values", {})
        IncrementExecute(new_values)
        return jsonify({"status": "success", "message": "Values updated successfully"}), 200
    except Exception:
        return jsonify({"status": "error", "message": "An error occurred"}), 500


@app.route('/loader', methods=["GET"])
def loader():
  filePath = "api/loader.lua"
  file = open(filePath, 'r')
  fileRead = file.read()
  return render_template("main.html", fileRead=fileRead)
