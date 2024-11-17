from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Load the merged county scores data with coordinates
with open('county_scores_with_coords.json', 'r') as f:
    county_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/county_data')
def county_data_endpoint():
    return jsonify(county_data)

if __name__ == '__main__':
    app.run(debug=True)