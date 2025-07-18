from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime 
import os

app = Flask(
    __name__,
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/static'))
)

posts = [
     {"id": 1, "title": "Welcome to EV Community", "content": "First post!", "votes": 5, "comments": []}
]

# stores registered users 
users = []
for u in users:
    if "favorites" not in u:
        u["favorites"] = []

# endpoint for user authentication 
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    display_name = data.get("display_name", username)
    bio = data.get("bio", "")
    location = data.get("location", "")
    interests = data.get("interests", [])
    social_links = data.get("social_links", {})
    # checking to see if user exists if not add to users list
    if any(u["username"] == username for u in users): 
        return jsonify({"error": "user already exists"}), 400
    users.append({
        "username": username, 
        "password": password,
        "display_name": display_name,
        "bio": bio, 
        "location": location, 
        "interests": interests,
        "social_links": social_links,
        "favorites": []
    })
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
            "user": data.get("user", "anonymous"),
            "comments": []
        }
        posts.append(new_post)
        return jsonify(new_post), 201
    # if request is GET, returns full list of posts sorted by vote count 
    else:
        search_term = request.args.get('search', '').lower()
        filtered_posts = posts
        if search_term:
            filtered_posts = [
                p for p in posts
                if search_term in p['title'].lower() or search_term in p['content'].lower()
            ]
        return jsonify(sorted(filtered_posts, key=lambda x: x['votes'], reverse=True))

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

# creating an endpoint for commenting system 
@app.route('/api/posts/<int:post_id>/comments', methods=['GET', 'POST'])
def post_comments(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return jsonify({"error": "post not found"}), 404
    if request.method == 'POST':
        data = request.json
        comment = {"user": data.get("user", "anonymous"), "content": data.get("content")}
        post.setdefault('comments', []).append(comment)
        return jsonify(comment), 201
    else:
        return jsonify(post.get('comments', []))

# adding endpoint for user post history system 
@app.route('/api/users/<username>/posts', methods=['GET'])
def user_posts(username):
    user_posts = [p for p in posts if p.get("user") == username]
    return jsonify(user_posts)

# adding enpoint to get the user info 
@app.route('/api/users/<username>/info', methods=['GET'])
def get_user_info(username):
    user = next((u for u in users if u["username"] == username), None)
    if not user:
        return jsonify({"error": "user not found"}), 404
    # Do not return password!
    return jsonify({
        "username": user["username"],
        "display_name": user.get("display_name", user["username"]),
        "bio": user.get("bio", ""),
        "location": user.get("location", ""),
        "interests": user.get("interests", []),
        "social_links": user.get("social_libnks", {})
    })

# update their profile description 
@app.route('/api/users/<username>/description', methods=['POST'])
def update_description(username):
    user = next((u for u in users if u["username"] == username), None)
    if not user:
        return jsonify({"error": "user not found"}), 404
    data = request.json
    new_description = data.get("description", "")
    user["description"] = new_description
    return jsonify({"message": "Description updated", "description": new_description})

# Get all favorite posts for a user
@app.route('/api/users/<username>/favorites', methods=['GET'])
def get_favorites(username):
    user = next((u for u in users if u["username"] == username), None)
    if not user:
        return jsonify({"error": "user not found"}), 404
    fav_posts = [p for p in posts if p["id"] in user["favorites"]]
    return jsonify(fav_posts)

# Add or remove a favorite post for a user
@app.route('/api/users/<username>/favorites/<int:post_id>', methods=['POST', 'DELETE'])
def modify_favorites(username, post_id):
    user = next((u for u in users if u["username"] == username), None)
    if not user:
        return jsonify({"error": "user not found"}), 404
    if request.method == 'POST':
        if post_id not in user["favorites"]:
            user["favorites"].append(post_id)
        return jsonify({"message": "Added to favorites"})
    elif request.method == 'DELETE':
        if post_id in user["favorites"]:
            user["favorites"].remove(post_id)
        return jsonify({"message": "Removed from favorites"})

if __name__ == '__main__':
    app.run(debug=True)
