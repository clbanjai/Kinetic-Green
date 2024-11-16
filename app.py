from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)


# Load state GeoJSON data

@app.route('/')
def index():
    return render_template('index.html')  # Assuming the HTML template is saved as 'index.html'

if __name__ == '__main__':
    app.run(debug=True)