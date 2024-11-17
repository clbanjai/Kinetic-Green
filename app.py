from flask import Flask,render_template

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')  # Assuming the HTML template is saved as 'index.html'

if __name__ == '__main__':
    app.run(debug=True)