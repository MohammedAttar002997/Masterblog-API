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
    if request.method == 'POST':
        # Get the new book data from the client
        new_post = request.get_json()
        if not validate_post_data(new_post):
            return jsonify({"error": "Invalid posts data"}), 400
            # Generate a new ID for the book
        new_id = max(book['id'] for book in POSTS) + 1
        new_post['id'] = new_id

        # Add the new book to our list
        POSTS.append(new_post)

        # Return the new book data to the client
        return jsonify(new_post), 201
    elif sort is not None or direction is not None:
        POSTS.sort(key=lambda x: x[sort], reverse = direction=='desc')
        return jsonify(POSTS), 200
    else:
        return jsonify(POSTS)

# def myFunc(e):
#   return e['year']
@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    # Find the book with the given ID
    post = find_post_by_id(id)

    # If the book wasn't found, return a 404 error
    if post is None:
        return 'Post with id {id} doesn\'t exist', 404

    # Update the book with the new data
    new_data = request.get_json()
    post.update(new_data)

    # Return the updated book
    return jsonify(post),200


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Find the book with the given ID
    post = find_post_by_id(id)

    # If the book wasn't found, return a 404 error
    if post is None:
        return f'Post with id {id} doesn\'t exist', 404
    if post["id"] == id:
        POSTS.remove(post)
    # Remove the book from the list
    # TODO: implement this
    ...

    # Return the deleted book
    return jsonify(f"Post with id {id} has been deleted successfully."),200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    query = request.args.get('title','content')
    # 2. Filter posts where query is in title OR content
    results = [
        post for post in POSTS
        if query in post['title'].lower() or query in post['content'].lower()
    ]
    return jsonify(results), 200



def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True


def find_post_by_id(post_id):
    """ Find the book with the id `book_id`.
    If there is no book with this id, return None. """
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
