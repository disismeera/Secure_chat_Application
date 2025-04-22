# Secure Chat Application

This is a Flask-based secure chat application that allows users to create or join chat rooms and exchange encrypted messages in real-time using Socket.IO.

## Features

- **User Identity**: Users can enter their name to start chatting.
- **Create or Join Chat Rooms**: Users can create new chat rooms or join existing ones using a unique code.
- **End-to-End Encryption**: Messages are encrypted using the `cryptography.fernet` library before being stored in the database.
- **Real-Time Messaging**: Messages are sent and received in real-time using Flask-SocketIO.
- **Persistent Storage**: Chat rooms and messages are stored in an SQLite database.

## Prerequisites

- Python 3.7 or higher
- Flask
- Flask-SocketIO
- cryptography
- SQLite3

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/secure-chat-app.git
    cd secure-chat-app
    ```

2. Install dependencies:
    ```bash
    pip install flask flask-socketio cryptography
    ```

3. Initialize the database:
    ```bash
    python -c "from app import init_db; init_db()"
    ```

## Usage

1. Run the application:
    ```bash
    python app.py
    ```

2. Open your browser and navigate to `http://127.0.0.1:5000`.

3. Enter your name and choose to either:
    - Create a new chat room.
    - Join an existing chat room using a unique code.

4. Start chatting securely in real-time!



## Security Notes

- The encryption key (`key`) is generated dynamically in this example. In production, store it securely (e.g., in an environment variable or a secure vault).
- Always sanitize user inputs to prevent XSS or SQL injection attacks.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

