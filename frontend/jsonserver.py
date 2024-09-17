from flask import Flask, jsonify, render_template_string
import json

app = Flask(__name__)

# Serve the HTML page
@app.route('/')
def index():
    return render_template_string(/home/nimnim/Xmaworld/frontend/test.html)  # You need to define `html_code` with your HTML content as a Python string.

# Serve the JSON data
@app.route('/data')
def data():
    # Open the JSON file and load its content
    with open('tutorials.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
