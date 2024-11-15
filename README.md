# Simple Password Manager

A secure and user-friendly command-line password manager to store, retrieve, and manage your passwords safely. The application encrypts your passwords using the **Fernet encryption** (a symmetric encryption technique), ensuring that your sensitive data remains protected.

## Features

- **Add Passwords**: Save website credentials securely.
- **Retrieve Passwords**: Decrypt and view stored passwords for specific usernames.
- **Delete Passwords**: Remove saved credentials from the database.
- **View All Passwords**: Display all stored credentials in a tabular format.
- **Encryption**: Uses a securely generated key to encrypt all stored passwords.
- **Backup System**: Automatically creates backups before modifying password files.
- **Error Handling**: Gracefully handles corrupted or empty files.

## Technologies Used

- **Python**: The programming language used for implementation.
- **Fernet Encryption**: Ensures secure storage of passwords.
- **Tabulate**: Displays passwords in a user-friendly table format.
- **JSON**: Used for storing passwords in a structured format.
- **Logging**: Provides detailed logs for debugging and tracking actions.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/password-manager.git
   cd password-manager
