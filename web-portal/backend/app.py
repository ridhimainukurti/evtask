from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

posts = [
     {"id": 1, "title": "Welcome to EV Community", "content": "First post!", "votes": 5}
]

@app.route('/api/posts', methods=['GET', 'POST'])
def get_or_add_posts():
    if request.method == 'POST':
        data = request.json
        new_post = {
            "id": len(posts) + 1,
            "title": data.get("title"),
            "content": data.get("content"),
            "votes": 0
        }
        posts.append(new_post)
        return jsonify(new_post), 201
    else:
        return jsonify(sorted(posts, key=lambda x: x['votes'], reverse=True))

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
