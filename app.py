from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# In-memory "database" to store users
# We'll use an integer ID as the key for easy lookup and management
users = {
    1: {"username": "alice", "email": "alice@example.com"},
    2: {"username": "bob", "email": "bob@example.com"}
}
# Variable to track the next available ID
next_id = 3

# --- API Endpoints ---

# 1. GET (All Users) - /users
@app.route('/users', methods=['GET'])
def get_all_users():
    """Returns a list of all users."""
    # Convert the dictionary of users into a list of user objects with their IDs
    user_list = [{"id": uid, **user_data} for uid, user_data in users.items()]
    return jsonify(user_list)

# 2. GET (Single User) - /users/<int:user_id>
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Returns a specific user by ID."""
    user_data = users.get(user_id)
    if user_data:
        # Include the ID in the response for clarity
        return jsonify({"id": user_id, **user_data})
    return jsonify({"message": f"User with ID {user_id} not found"}), 404

# 3. POST (Create User) - /users
@app.route('/users', methods=['POST'])
def create_user():
    """Creates a new user."""
    global next_id
    
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    new_user_data = request.get_json()
    
    # Basic validation for required fields
    if 'username' not in new_user_data or 'email' not in new_user_data:
        return jsonify({"message": "Missing 'username' or 'email' in JSON"}), 400
    
    # Assign the new user the next ID and store it
    users[next_id] = new_user_data
    created_id = next_id
    next_id += 1 # Increment the ID counter for the next new user
    
    # Return the created user's data and a 201 Created status code
    return jsonify({"message": "User created successfully", "id": created_id, **new_user_data}), 201

# 4. PUT (Update User) - /users/<int:user_id>
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates an existing user by ID."""
    user_data = users.get(user_id)
    if not user_data:
        return jsonify({"message": f"User with ID {user_id} not found"}), 404
        
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    update_data = request.get_json()
    
    # Update only the fields provided in the request
    if 'username' in update_data:
        users[user_id]['username'] = update_data['username']
    if 'email' in update_data:
        users[user_id]['email'] = update_data['email']
        
    return jsonify({"message": f"User with ID {user_id} updated successfully", **users[user_id]})

# 5. DELETE (Delete User) - /users/<int:user_id>
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user by ID."""
    if user_id in users:
        del users[user_id]
        return jsonify({"message": f"User with ID {user_id} deleted successfully"}), 204 # 204 No Content
    return jsonify({"message": f"User with ID {user_id} not found"}), 404

# Run the application
if __name__ == '__main__':
    # Setting debug=True restarts the server automatically on code changes
    app.run(debug=True)