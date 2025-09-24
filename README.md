Flask Notes Manager

A web-based notes management application built with Flask, allowing users to register, login, add, edit, delete, search, and export notes. Users can also upload files and securely manage their accounts.

Features

User registration with email verification (OTP)

Secure login with hashed passwords

Add, edit, delete, and view notes

Search notes by title or content

Export notes as TXT files

Upload and view files

Session-based authentication to protect endpoints

Fully responsive HTML templates

Tech Stack

Backend: Python, Flask

Database: MySQL (can be PlanetScale or local)

Frontend: HTML, CSS, Jinja2 templates

Email: Yagmail (SMTP) for OTP verification

Installation

Clone the repository:

git clone https://github.com/<your-username>/<repo>.git
cd <repo>


Create a virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Create a .env file (example .env.example provided) with the following variables:

SECRET_KEY=your_flask_secret_key
EMAIL_USER=your_email
EMAIL_PASS=your_email_password
DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASS=your_db_password
DB_NAME=your_db_name


Run the app locally:

python app.py


Open http://127.0.0.1:5030 in your browser.

Database Setup

The app will automatically create tables (USERS, NOTES, FILES) if they don’t exist.

Make sure your database is running and credentials in .env are correct.

Usage

Register a new user → Verify email via OTP

Login with username and password

Use dashboard to:

Add notes

View, edit, or delete notes

Upload and view files

Export notes as TXT files

Search notes

Project Structure
.
├── app.py                  # Main Flask application
├── database.py             # Database connection & queries
├── config.py               # Secrets & email credentials
├── requirements.txt        # Python dependencies
├── uploads/                # Uploaded files
├── templates/              # HTML templates
└── static/                 # CSS, JS, images

Security

Passwords are hashed using Werkzeug.

All sensitive data is stored in environment variables.

Session-based authentication protects endpoints.
