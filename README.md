# ☁️ Cloud-Based File Storage System

A Flask-based web application that lets users securely upload, download, and share files through integration with Google Drive. The system supports user authentication, session handling, and file sharing via unique shareable links with expiration.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture Overview](#architecture-overview)
- [Folder Structure](#folder-structure)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Contributors](#contributors)
- [License](#license)

---

## Features

- User Registration & Login (Flask-Login)
- File Upload (Google Drive Integration)
- File Download
- File Sharing with Expiration
- REST API Support (cURL/Postman)
- Web-Based Interface with Upload/Share Forms

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
+--------------------+          +--------------------+
| Flask Blueprints   |          |  Google Drive API  |
| (Auth & Files)     |--------->|  Upload/Download   |
+--------+-----------+          +--------------------+
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


 
