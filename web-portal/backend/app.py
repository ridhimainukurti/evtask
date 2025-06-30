from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/posts')
def get_posts():
    return jsonify([
        {"id": 1, "title": "Welcome to EV Community", "content": "First post!", "votes": 5}
    ])

if __name__ == '__main__':
    app.run(debug=True)
