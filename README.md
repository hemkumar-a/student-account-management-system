# Student Account Management System

A Django-based web application for managing student accounts and academic information through role-aware dashboards, course management, course registration, results processing, and transcript generation.

## Overview

The project provides a centralized academic portal for students and staff. Students can create and manage their accounts, view academic information, register for courses, and review results. Staff users can manage student records, courses, academic programs, and result data.

## Key Features

### Authentication & Student Accounts
- Email-based authentication with a custom Django user model
- Student registration and profile management
- Staff/admin dashboard for student administration
- Student status management

### Academic Management
- Department and academic-program management
- Course creation, editing, and deletion
- Course allocation and registration
- Result entry and assessment workflows

### Student Performance
- Result listing and detail views
- Performance analysis
- Transcript generation
- CGPA/GPA-oriented academic summaries

### Interface
- Responsive Django templates
- Shared base layout
- Static CSS and JavaScript
- Separate student and staff dashboard experiences

## Technology Stack

- Python
- Django
- HTML5
- CSS3
- JavaScript
- SQLite for local development

## Application Flow

```
Authentication → Dashboard → Student/Course Management → Registration → Results → Performance → Transcript
```

## Project Structure

```
student-account-management-system/
├── apps/
│   ├── accounts/
│   ├── core/
│   ├── course/
│   └── result/
├── config/
├── templates/
├── static/
├── screenshots/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Screenshots

### Login
![Login](screenshots/01-login.png)

### Student Dashboard
![Student Dashboard](screenshots/02-student-dashboard.png)

### Admin Dashboard
![Admin Dashboard](screenshots/03-admin-dashboard.png)

### Results
![Results](screenshots/04-results.png)

## Local Setup

### 1. Clone the repository

```
git clone https://github.com/hemkumar-a/student-account-management-system.git
cd student-account-management-system
```

### 2. Create and activate a virtual environment

Windows:
```
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Apply migrations

```
python manage.py migrate
```

### 5. Create an admin account

```
python manage.py createsuperuser
```

### 6. Start the development server

```
python manage.py runserver
```

Open the local Django development URL shown in the terminal.

## Notes

- The repository intentionally excludes the local SQLite database and Python cache files.
- Use a local development database for testing.
- Review Django settings before deploying to production; production deployments should use environment-based secrets, secure secret-key management, HTTPS, and an appropriate production database.

## Project Highlights

This project demonstrates practical experience with Django application structure, custom authentication, relational data modelling, role-aware workflows, CRUD operations, templates, static assets, academic result processing, and transcript-oriented reporting.

## License

No open-source license is granted by default. Contact the repository owner before reusing, redistributing, or publishing derived versions of this project.