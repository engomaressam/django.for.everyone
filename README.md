# Django for Everyone - Assignment 01

This repository contains the Django project for Assignment 01 of the Django for Everyone course.

## Project Structure

- `mysite/` - Main Django project directory
  - `mysite/` - Project settings and configuration
  - `polls/` - Polls application
- `m01/`, `m02/`, `m03/`, `m04/`, `m05/` - Course module directories
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore file

## Setup Instructions

### Local Development

1. Create and activate a virtual environment:
   ```bash
   python -m venv .ve52
   # On Windows:
   .\.ve52\Scripts\Activate.ps1
   # On macOS/Linux:
   source .ve52/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   cd mysite
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000/polls/` to see the application.

## Assignment Requirements

- ✅ Django 5.2 installed
- ✅ Virtual environment created
- ✅ Polls app created with required string "69459307"
- ✅ ALLOWED_HOSTS configured for deployment
- ✅ URL routing configured

## Deployment

This project is configured for deployment to PythonAnywhere via GitHub. The `ALLOWED_HOSTS` setting is configured to allow all hosts for deployment purposes.

## Course Information

This project is part of the Django for Everyone course (DJ4E) and includes the required assignment string "69459307" in the polls index view.
