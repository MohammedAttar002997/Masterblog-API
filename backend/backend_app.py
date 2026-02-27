import logging
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    app.logger.info('GET request received for /api/posts')
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    # Requirement: Invalid direction values must return a 400
    if direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid direction. Must be 'asc' or 'desc'."}), 400
    # Requirement: Handle empty list case
    if not POSTS:
        return jsonify([])

    if request.method == 'POST':
        # Get the new post data from the client
        new_post = request.get_json()
        if not validate_post_data(new_post):
            return jsonify({"error": "Invalid posts data"}), 400
            # Generate a new ID for the post
        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id

        # Add the new post to our list
        POSTS.append(new_post)

        # Return the new post data to the client
        return jsonify(new_post), 201
    elif sort:
        if sort not in ['title', 'content']:
            return jsonify({"error": f"Invalid sort field: {sort}"}), 400

        reverse = (direction == 'desc')
        sorted_posts = sorted(POSTS, key=lambda x: x[sort].lower(), reverse=reverse)
        return jsonify(sorted_posts)
    return jsonify(POSTS)


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    # Find the post with the given ID
    post = find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        return 'Post with id {id} doesn\'t exist', 404

    # Update the post with the new data
    new_data = request.get_json()
    post.update(new_data)

    # Return the updated post
    return jsonify(post),200


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Find the post with the given ID
    post = find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        return f'Post with id {id} doesn\'t exist', 404
    if post["id"] == id:
        POSTS.remove(post)
    # Remove the post from the list
    # TODO: implement this
    ...

    # Return the deleted post
    return jsonify(f"Post with id {id} has been deleted successfully."),200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    # Read parameters separately
    title = request.args.get('title','')
    content = request.args.get('content','')

    filtered_posts = []

    for post in POSTS:
        # Check if title matches (if title param provided)
        title_match = title in post['title'].lower() if title else True
        # Check if content matches (if content param provided)
        content_match = content in post['content'].lower() if content else True

        if title_match and content_match:
            # Avoid returning everything if both params are empty (optional, depending on preference)
            if not title and not content:
                continue
            filtered_posts.append(post)
    return jsonify(filtered_posts), 200


def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True


def find_post_by_id(post_id):
    """ Find the post with the id `post_id`.
    If there is no post with this id, return None. """
    post_to_update = next((post for post in POSTS if post['id'] == post_id), None)
    # TODO: implement this
    return post_to_update


def find_post_by_title(title):
    post_to_update = next((post for post in POSTS if post['title'] == title), None)
    # TODO: implement this
    return post_to_update


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": error}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": error}), 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
