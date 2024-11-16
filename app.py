from flask import Flask, render_template
import json

app = Flask(__name__)

# Load GeoJSON data
with open('json/geo.json') as f:
    geojson_data = json.load(f)

@app.route('/')
def home():
    return render_template('index.html', geojson_data=json.dumps(geojson_data))

if __name__ == '__main__':
    app.run(debug=True)