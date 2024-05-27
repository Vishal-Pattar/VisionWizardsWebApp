import json

def load_users():
    """
    Load users from the JSON file.

    :return: List of users
    """
    with open('users.json', 'r') as file:
        users = json.load(file)
    return users

def login_user(email, password):
    """
    Function to handle user login.

    :param email: User's email
    :param password: User's password
    :return: Boolean indicating whether login is successful
    """
    users = load_users()
    for user in users:
        if user["email"] == email and user["password"] == password:
            return True
    return False