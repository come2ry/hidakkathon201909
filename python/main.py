from flask import Flask, abort
app = Flask(__name__)

@app.route('/<path>')
def index(path):
    abort(501)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

