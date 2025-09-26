from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory dictionary to store users
users = {}
user_id_counter = 1

@app.route('/users', methods=['GET'])
def get_users():
    """Retrieves all users."""
    return jsonify(list(users.values()))

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a single user by ID."""
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """Creates a new user."""
    global user_id_counter
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({"message": "Username and email are required"}), 400

    new_user = {
        "id": user_id_counter,
        "username": data['username'],
        "email": data['email']
    }
    users[user_id_counter] = new_user
    user_id_counter += 1
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates an existing user."""
    user = users.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided for update"}), 400

    user.update(data)
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user."""
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)