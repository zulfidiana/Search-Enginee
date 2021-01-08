from flask import Flask, render_template, jsonify
from query import Search

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/<search>/<jumlah>')
def search(search, jumlah):
    result = Search().search(search, int(jumlah))
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)