try:
    username = input("Username: ")
    password = input("Password: ")

    if password != "admin123":
        raise ValueError("Incorrect password.")
    
    print(f"Welcome, {username}!")

except ValueError as e:
    print(f"Error: {e}")