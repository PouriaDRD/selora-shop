# Selora Shop Backend

Selora Backend is the Django-based REST API powering the Selora Shop e-commerce platform. It handles authentication, user accounts, cart operations, and store-related business logic for the frontend application.

## Overview

This backend provides a modular API layer for:

- user registration and authentication
- JWT-based session management
- cart and order-related operations
- media storage for product and variant images
- API documentation and error handling

## Tech Stack

- Python 3.11+
- Django 6
- Django REST Framework
- Simple JWT
- drf-spectacular for API schema documentation
- django-cors-headers
- django-filter
- SQLite by default for local development
- pytest for testing

## Project Structure

```text
selora-backend/
├── accounts/             # User account models, services, repositories, validators
├── authentication/      # Login history and auth-related services
├── cart/                 # Cart models, services, and repositories
├── config/               # Django settings, URLs, exception handling, Swagger config
├── media/                # Uploaded images and media files
├── store/                # Store app for products and related business logic
├── manage.py             # Django management entrypoint
├── requirements.txt      # Python dependencies
└── dev_db.sqlite3        # Local development database
```

## Features

- JWT authentication flow
- user and login history management
- reusable repository/service patterns for business logic
- API schema generation with Swagger-compatible docs
- local media handling for product and variant images

## Requirements

Make sure you have:

- Python 3.11 or newer
- pip
- virtual environment support

Check your Python version:

```bash
python --version
```

## Getting Started

1. Create and activate a virtual environment:

```bash
cd selora-backend
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux, use:

```bash
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

The project includes example environment files:

```bash
copy .env.example .env
```

If needed, adjust the values for your local setup.

4. Run database migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## API Documentation

Swagger and schema endpoints are available through the configured API documentation setup.

Typical endpoints include:

- `/api/schema/`
- `/api/docs/`
- `/api/redoc/`

## Testing

Run the test suite with:

```bash
pytest
```

## Useful Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
```

## Notes

- The project is configured for local development using SQLite.
- Media uploads are stored under the `media/` directory.
- The codebase follows a service/repository-oriented structure to keep domain logic organized.
