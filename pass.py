import os
import json
import base64
from cryptography.fernet import Fernet
from tabulate import tabulate
import shutil  # For creating backups
import logging  # For logging actions

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Paths
PASSWORDS_DIR = "D:/passwords"
KEY_FILE = os.path.join(PASSWORDS_DIR, "secret.key")
PASSWORD_FILE = os.path.join(PASSWORDS_DIR, "passwords.json")
BACKUP_FILE = os.path.join(PASSWORDS_DIR, "passwords_backup.json")


# Utility Functions
def ensure_directory_exists():
    if not os.path.exists(PASSWORDS_DIR):
        os.makedirs(PASSWORDS_DIR)


def backup_password_file():
    """Create a backup of the passwords file before modifying it."""
    if os.path.exists(PASSWORD_FILE):
        shutil.copy(PASSWORD_FILE, BACKUP_FILE)
        logging.info("Backup of passwords.json created.")


def load_data():
    """Load data from the passwords file."""
    if not os.path.exists(PASSWORD_FILE):
        return {}
    try:
        with open(PASSWORD_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.warning("Password file corrupted or empty. Returning empty data.")
        return {}


def save_data(data):
    """Save data to the passwords file."""
    backup_password_file()
    with open(PASSWORD_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Key Management
def generate_key():
    """Generate a new encryption key."""
    return Fernet.generate_key()


def save_key(key):
    """Save the encryption key to a file."""
    ensure_directory_exists()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)


def load_key():
    """Load the encryption key from file."""
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("Encryption key not found. Run the program to generate one.")
    return open(KEY_FILE, "rb").read()


# Encryption/Decryption
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())


def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()


# Password Management
def save_password(website, username, password, key):
    data = load_data()
    encrypted_password = encrypt_password(password, key)
    encrypted_password_str = base64.urlsafe_b64encode(encrypted_password).decode()
    data[username] = {"website": website, "password": encrypted_password_str}
    save_data(data)
    logging.info(f"Password for {username} on {website} saved.")


def get_password(username, key):
    data = load_data()
    if username in data:
        info = data[username]
        encrypted_password = base64.urlsafe_b64decode(info["password"])
        password = decrypt_password(encrypted_password, key)
        return info["website"], password
    logging.warning(f"No password found for username: {username}")
    return None


def delete_password(username):
    data = load_data()
    if username in data:
        del data[username]
        save_data(data)
        logging.info(f"Password for {username} deleted.")
    else:
        logging.warning(f"No password found for username: {username}")


def view_all_passwords(key):
    data = load_data()
    if not data:
        print("No passwords stored yet.")
        return

    table_data = []
    for username, info in data.items():
        encrypted_password = base64.urlsafe_b64decode(info["password"])
        decrypted_password = decrypt_password(encrypted_password, key)
        table_data.append([info["website"], username, decrypted_password])

    print("\nAll Stored Passwords:")
    print(tabulate(table_data, headers=["Website", "Username", "Password"], tablefmt="grid"))


# Main User Interface
def main():
    print("Simple Password Manager")
    ensure_directory_exists()

    # Load or generate the encryption key
    if os.path.exists(KEY_FILE):
        key = load_key()
    else:
        key = generate_key()
        save_key(key)
        print("Encryption key generated and saved.")

    while True:
        print("\nSelect an option:")
        print("1. Add a new password")
        print("2. View a password")
        print("3. Delete a password")
        print("4. View all stored passwords")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            website = input("Enter website name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            save_password(website, username, password, key)
            print(f"Password for {username} on {website} saved.")

        elif choice == "2":
            username = input("Enter username: ")
            result = get_password(username, key)
            if result:
                website, password = result
                print(f"Website: {website}\nPassword for {username}: {password}")

        elif choice == "3":
            username = input("Enter username to delete: ")
            delete_password(username)

        elif choice == "4":
            view_all_passwords(key)

        elif choice == "5":
            print("Exiting password manager.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
