def login_user(email, password):
    """
    Function to handle user login.

    :param email: User's email
    :param password: User's password
    :return: Boolean indicating whether login is successful
    """
    # In a real application, add authentication logic here
    return email == "admin@mahametro.com" and password == "admin123"