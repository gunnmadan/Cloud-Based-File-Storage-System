# ☁️ Cloud-Based File Storage System

The Cloud-Based File Storage System is a secure, lightweight web application built with Flask that enables users to upload, download, and share files easily through a personal account-based system. Designed for simplicity and modularity, this application replicates the core functionalities of large-scale cloud storage providers while remaining small, transparent, and educational. It offers an intuitive user experience, focusing on core operations like secure login, file management, and generating shareable download links that do not require an account for access.

This project was developed to deepen understanding of full-stack web development concepts, particularly around backend authentication, file system management, database operations, and secure data handling. By utilizing a MySQL database in combination with SQLAlchemy ORM, the system efficiently stores and retrieves user information and file metadata. The application currently stores uploaded files locally, but its modular design allows easy extension to integrate external cloud storage services in future iterations. Whether used as a foundation for more complex systems or as a standalone solution for secure file management, the Cloud-Based File Storage System offers a practical, extensible model for lightweight cloud infrastructure development.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture Overview](#architecture-overview)
- [Folder Structure](#folder-structure)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [API Endpoints](#api-endpoints)
- [Contributors](#contributors)
  
---

## Features

Users can create an account, securely log in, and manage their personal file storage. Uploaded files are saved to the server and linked to the user’s account through the database. Files can be downloaded at any time and can also be shared externally through secure links that do not require a recipient to log in. Access control and file integrity are enforced throughout the system to ensure user data remains protected.

The system is structured modularly, separating application logic, database models, routing, and front-end templates for clarity and maintainability. Passwords are securely hashed before storage, and protected routes ensure that only authenticated users can interact with sensitive actions.

---

## Tech Stack

- **Frontend**: HTML, CSS, Jinja2
- **Backend**: Flask (Python)
- **Database**: MySQL with SQLAlchemy ORM
- **Auth**: Flask-Login
- **Cloud Storage**: Google Drive API (OAuth2)
- **Others**: PyMySQL, Flask Blueprints

---

## Architecture Overview

```text
+-------------+
|   Browser   |  ← User Interface (HTML templates)
+------+------+ 
       |
       v
+-------------+
|   Flask App |  ← Handles routing, auth, and logic
+------+------+ 
       |
       v
+--------------------+
| Flask Blueprints   |
| (Auth & Files)     |
+--------+-----------+
         |
         v
+------------------+
|  SQLAlchemy ORM  | ← Communicates with MySQL
+--------+---------+
         |
         v
+------------------+
|   MySQL Database |
+------------------+
```

The application follows a modular MVC-inspired structure. User requests are routed through Flask endpoints, invoking database operations managed via SQLAlchemy models. Files are uploaded securely to a server-side directory, and associated metadata, including user ownership and shareable tokens, is stored in MySQL tables. The front-end templates dynamically render user-specific views based on authenticated sessions. Secure sharing links are generated with unique tokens to control access without requiring account login from recipients.

---

## Folder Structure

The project is organized to maintain a clean separation between components. The `/app` directory contains the application factory, authentication routes, file management routes, and database models. HTML templates for user-facing pages are located in `/templates`, and static assets such as CSS files are stored in `/static`. Uploaded files are saved to a secure `/uploads` directory on the server. Configuration settings are managed in the main application file.

---

## Setup Instructions

To set up the Cloud-Based File Storage System locally, begin by cloning the repository to your machine using Git. Open your terminal, navigate to the directory where you want to place the project, and run git clone <repository_link>. After cloning, navigate into the project folder using cd Cloud-Based-File-Storage-System.

Ensure you have Python installed on your system. It is recommended to use a virtual environment to manage dependencies and avoid conflicts. Create and activate a virtual environment by running python -m venv venv followed by source venv/bin/activate on macOS/Linux or venv\\Scripts\\activate on Windows.

Once inside the virtual environment, install all required Python packages by executing pip install -r requirements.txt. This will install Flask, SQLAlchemy, Flask-Login, PyMySQL, and any other dependencies necessary for running the application.

Before launching the application, set up a MySQL database. Create a new database instance locally, and update the database URI in the application's configuration file to include your MySQL username, password, and database name. The database connection string typically follows the format mysql+pymysql://username:password@localhost/databasename.

With the database configured, initialize the database tables. You can achieve this by opening a Flask shell (flask shell) and running the db.create_all() command to create the necessary schema based on the defined models. Alternatively, you may execute any provided database setup scripts.

After completing these setup steps, you are ready to run the application. Start the Flask development server by running flask run in your terminal. The server will launch locally, typically accessible via http://127.0.0.1:5000/ in your browser. From there, you can register a new user, log in, and start uploading, downloading, and sharing files securely.

---

## Usage Guide

Once the application is running locally, users are greeted with a login page. If a user does not yet have an account, they can navigate to the registration page and create a new account by providing a username, a valid email address, and a secure password. Upon successful registration, users are redirected to the login page to authenticate themselves using their new credentials. After logging in, users are taken to their personal dashboard. From the dashboard, users can upload files directly from their local machine. Each uploaded file is securely saved on the server and recorded in the MySQL database along with metadata such as the original filename and ownership information. Users can view a list of all files they have uploaded, download any of their files, or delete them if necessary. The system also allows users to generate a secure shareable link for any uploaded file. By selecting the "Share" option next to a file, the system creates a unique time-limited link that can be shared with others. Recipients with the link can download the shared file without needing to create an account, making file sharing simple and efficient while maintaining access control through token validation.

Users can log out at any time to end their session securely. Once logged out, access to protected resources is restricted until the user logs in again. The system provides clear feedback and prompts throughout all user actions, ensuring a smooth, intuitive experience from account creation to file management and sharing.

---

## API Endpoints

The application exposes several key routes to manage user actions and file storage:

- `/register`: Handles new user registrations.
- `/login`: Authenticates users and creates sessions.
- `/logout`: Ends the user's session.
- `/upload`: Accepts file uploads for authenticated users.
- `/download/<file_id>`: Retrieves files for download by the owner.
- `/share/<file_id>`: Generates a secure, time-limited share link for a file.
- `/shared/<token>`: Allows public access to a file via a valid share token.

All sensitive actions are protected behind authentication middleware except for shared link access, which uses token validation to control external downloads.

## Contributors

This project was developed by Gunn Madan, Miracle Emefiele, Morewa Omolabi, and Ethan Munji as part of a cloud computing project course. Contributions included backend development, database design, authentication setup, file storage handling, and front-end template design. The system architecture and implementation were guided with feedback from the course instructor.

