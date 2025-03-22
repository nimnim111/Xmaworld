from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

UPLOAD_FOLDER = os.path.join('static')
IMAGE_FOLDER = os.path.join(UPLOAD_FOLDER, 'images')
VIDEO_FOLDER = os.path.join(UPLOAD_FOLDER, 'videos')
JSON_FILE = 'tricks_data.json'

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

def init_json_file():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w') as f:
            json.dump({"tricks": []}, f, indent=4)

def load_json_data():
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"tricks": []}
        with open(JSON_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return data

def save_json_data(data):
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def generate_unique_filename(filename):
    timestamp = datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss")
    return f"{timestamp}_{secure_filename(filename)}"

@app.route('/')
def index():
    q = request.args.get('q', '').strip().lower()

    data = load_json_data()
    all_tricks = data["tricks"]

    if q:
        tricks = [trick for trick in all_tricks if q in trick["name"].lower()]
    else:
        tricks = all_tricks

    return render_template('index.html', tricks=tricks)

@app.route('/add')
def add_trick_form():
    return render_template('add_trick.html')

@app.route('/add_trick', methods=['POST'])
def add_trick():
    trick_name = request.form.get('trick_name', '').strip()
    athlete = request.form.get('athlete', '').strip()
    description = request.form.get('description', '').strip()

    if not trick_name or not athlete or not description:
        flash("Please fill out Trick Name, Athlete, and Description.")
        return redirect(url_for('add_trick_form'))

    image_file = request.files.get('image_file')
    video_file = request.files.get('video_file')

    if not image_file or image_file.filename == "":
        flash("An image file is required.")
        return redirect(url_for('add_trick_form'))

    if not video_file or video_file.filename == "":
        flash("A video file is required.")
        return redirect(url_for('add_trick_form'))

    data = load_json_data()
    for existing_trick in data["tricks"]:
        if existing_trick["name"].lower() == trick_name.lower():
            flash(f"A trick named '{trick_name}' already exists!")
            return redirect(url_for('add_trick_form'))

    image_filename = generate_unique_filename(image_file.filename)
    image_path = os.path.join('images', image_filename)
    image_file.save(os.path.join(IMAGE_FOLDER, image_filename))

    video_filename = generate_unique_filename(video_file.filename)
    video_path = os.path.join('videos', video_filename)
    video_file.save(os.path.join(VIDEO_FOLDER, video_filename))

    slug = trick_name.lower().replace(' ', '-')
    new_trick = {
        "id": str(uuid.uuid4()),
        "name": trick_name,
        "athlete": athlete,
        "textdesc": description,
        "image": image_path,
        "videofile": video_path,
        "link": f"/{slug}",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data["tricks"].append(new_trick)
    save_json_data(data)

    flash("Trick added successfully!")
    return redirect(url_for('index'))

@app.route('/<trick_slug>')
def trick_detail(trick_slug):
    data = load_json_data()
    found_trick = None
    for t in data["tricks"]:
        if t["link"] == f"/{trick_slug}":
            found_trick = t
            break

    if found_trick:
        return render_template('trick_detail.html', trick=found_trick)
    else:
        return "Trick not found", 404

if __name__ == '__main__':
    init_json_file()
    app.run(debug=True)
