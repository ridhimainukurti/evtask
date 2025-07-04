from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(
    __name__,
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/static'))
)

posts = [
     {"id": 1, "title": "Welcome to EV Community", "content": "First post!", "votes": 5}
]

# stores registered users 
users = []
# endpoint for user authentication 
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    # checking to see if user exists if not add to users list
    if any(u["username"] == username for u in users): 
        return jsonify({"error": "user already exists"}), 400
    users.append({"username": username, "password": password})
    return jsonify({"message": "registered"})

@app.route('/api/login', methods=['POST'])   
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    # check the username and password exists in users 
    for user in users: 
        if user["username"] == username and user["password"] == password:
            return jsonify({"message": "logged in", "username": username})
    return jsonify({"error": "invalid credentials"}), 401

# endpoint for adding or viewing posts 
@app.route('/api/posts', methods=['GET', 'POST'])
def get_or_add_posts():
    if request.method == 'POST':
        data = request.json
        # creates new dictionary for new post 
        new_post = {
            "id": len(posts) + 1,
            "title": data.get("title"),
            "content": data.get("content"),
            "votes": 0,
            "user": data.get("user", "anonymous")
        }
        posts.append(new_post)
        return jsonify(new_post), 201
    # if request is GET, returns full list of posts sorted by vote count 
    else:
        return jsonify(sorted(posts, key=lambda x: x['votes'], reverse=True))

# new post endpoint 
@app.route('/api/posts/<int:post_id>/vote', methods=['POST'])
def vote_post(post_id):
    data = request.json
    action = data.get("action")
    # finds post by id, changes the votes and returns updated post 
    for post in posts: 
        if post["id"] == post_id:
            if action == "upvote":
                post["votes"] += 1
            elif action == "downvote":
                post["votes"] -= 1
            return jsonify(post)
    return jsonify({"error": "post not found"}), 404

# admin dashboard endpoint to remove posts
@app.route('/api/posts/<int:post_id>/delete', methods=['DELETE'])
def delete_posts(post_id):
    global posts
    # checking if the admin is in the query string 
    username = request.args.get("admin")
    if username != "admin":
        return jsonify({"error": "not authorized"}), 401
    # removes post with the given post id and returns a message
    posts = [p for p in posts if p["id"] != post_id]
    return jsonify({"message": "deleted"})

@app.route('/')
def index():
    #return send_from_directory('../frontend', 'index.html')
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend')), 'index.html')

@app.route('/static/<path:filename>')
def send_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
