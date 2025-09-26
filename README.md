📝 Flask Notes Manager

A web-based notes management application I built with Flask, enabling users to securely create, manage, search, and export notes. Users can also upload files and manage their accounts seamlessly.








🚀 Features I Implemented

✅ User registration with email OTP verification

✅ Secure login with hashed passwords

✅ Add, edit, delete, and view notes

✅ Search notes by title or content

✅ Export notes as TXT files

✅ Upload and view files

✅ Session-based authentication to protect data

✅ Fully responsive HTML templates

🛠 Tech Stack

Backend: Python, Flask

Database: MySQL (PlanetScale or local)

Frontend: HTML, CSS, Jinja2 templates

Email: Yagmail (SMTP) for OTP verification

⚡ Installation & Setup

I designed the app to run locally using Python. Here’s how I set it up:

git clone https://github.com/<your-username>/<repo>.git
cd <repo>
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt


Create a .env file with your credentials (I used an example .env.example):

SECRET_KEY=your_flask_secret_key
EMAIL_USER=your_email
EMAIL_PASS=your_email_password
DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASS=your_db_password
DB_NAME=your_db_name


Run the app:

python app.py


Open http://127.0.0.1:5030
 in your browser.

🗄 Database Design

I structured the database with three tables:

Table	Purpose
USERS	Stores user credentials securely
NOTES	Stores notes with timestamps
FILES	Manages uploaded files and metadata

I used PyMySQL for database interactions and foreign keys for relational integrity.

🎨 How I Built It

Managed user sessions with Flask sessions

Used Werkzeug to hash passwords

Handled file uploads & downloads with Flask’s send_file

Implemented search functionality across notes

Built a responsive UI with HTML & CSS

Added email OTP verification using Yagmail for registration & password reset

☁ Deployment

I made the app deploy-ready on pythonanywhere.com, using environment variables for secure credentials and connecting MySQL databases.

🗂 Project Structure
.
├── app.py                  # Main Flask app
├── database.py             # DB connection & queries
├── config.py               # Secrets & email credentials
├── requirements.txt        # Python dependencies
├── uploads/                # Uploaded files
├── templates/              # HTML templates
└── static/                 # CSS, JS, images
