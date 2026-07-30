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

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Environment Variables

Create a `.env` file in the backend folder using the example file as a starting point:

```bash
copy .env.example .env
```

Common variables include:

```env
DEBUG="True"

BASE_URL="api/"
ADMIN_URL="admin/"

SECRET_KEY="your-secret-key"

# ---------------------------------------------------------------
# Internationalization Configuration
# ---------------------------------------------------------------
LANGUAGE_CODE="en-us"
TIME_ZONE="Asia/Tehran"

USE_I18N="False"
USE_TZ="True"


# ---------------------------------------------------------------
# AUTH Configuration
# ---------------------------------------------------------------
# expire after n minutes
ACCESS_TOKEN_LIFETIME="60"
# expire after n days 
REFRESH_TOKEN_LIFETIME="7"  

# ---------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------
# Set USE_SQLITE=True for local development without PostgreSQL
USE_SQLITE="True"

DB_NAME="selora_shop"
DB_USER="user"
DB_PASSWORD="strong_password_123"
DB_HOST="localhost"
DB_PORT="5432"

# ===================================================================
# Django Networking, CORS & Security Configuration
# ===================================================================
#
# These settings control:
#   • Which hosts can access Django
#   • Which frontend applications can communicate with the API
#   • Which origins are trusted for CSRF validation
#   • Which IPs are considered internal (Debug Toolbar, etc.)
#
# Values are comma-separated.
#
# Example:
#
#   localhost
#   127.0.0.1
#   192.168.1.2
#   api.example.com
#   shop.example.com
#
# ===================================================================



# -------------------------------------------------------------------
# Internal IP Addresses
# -------------------------------------------------------------------
#
# Used by packages such as:
#   - django-debug-toolbar
#   - internal debugging middleware
#
# These IP addresses are considered trusted only for development.
#
# Example:
# INTERNAL_IPS="127.0.0.1,192.168.1.5,10.0.0.15"
#
INTERNAL_IPS="localhost,127.0.0.1,192.168.1.2"



# -------------------------------------------------------------------
# Allowed Hosts
# -------------------------------------------------------------------
#
# SECURITY CRITICAL
#
# Django will reject requests whose Host header is not listed here.
#
# Include every hostname or IP address that can access your backend.
#
# Development Example:
#
# ALLOWED_HOSTS="localhost,127.0.0.1,192.168.1.2"
#
# Production Example:
#
# ALLOWED_HOSTS="api.example.com,example.com"
#
ALLOWED_HOSTS="localhost,127.0.0.1,192.168.1.2"



# -------------------------------------------------------------------
# Allow Cookies & Authorization Headers in Cross-Origin Requests
# -------------------------------------------------------------------
#
# When True:
#
# - Cookies are allowed.
# - Session authentication works.
# - JWT inside cookies works.
# - Authorization headers are allowed.
#
# Usually:
#
# Development  -> True
# Production   -> True (if frontend/backend are on different domains)
#
CORS_ALLOW_CREDENTIALS="True"



# -------------------------------------------------------------------
# Allowed CORS Origins
# -------------------------------------------------------------------
#
# SECURITY CRITICAL
#
# Only these frontend origins may send requests to your API.
#
# Each origin MUST include:
#
#   protocol + host + optional port
#
# Valid:
#
#   http://localhost:3000
#   http://127.0.0.1:3000
#   http://192.168.1.2:3000
#   https://app.example.com
#
# Invalid:
#
#   localhost
#   192.168.1.2
#   example.com
#
# If your Next.js app runs on port 3000,
# DO NOT forget to include the port.
#
CORS_ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000,http://192.168.1.2:3000"



# -------------------------------------------------------------------
# Trusted CSRF Origins
# -------------------------------------------------------------------
#
# Required when using:
#
# - Django Session Authentication
# - CSRF Protection
# - Cookies
# - Admin Panel
#
# Format is identical to CORS_ALLOWED_ORIGINS.
#
# Example:
#
# CSRF_TRUSTED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
#
# Production Example:
#
# CSRF_TRUSTED_ORIGINS="https://app.example.com"
#
CSRF_TRUSTED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000,http://192.168.1.2:3000"
```

### Key variables

- `DEBUG`: enables or disables Django debug mode.
- `SECRET_KEY`: secret key used by Django.
- `USE_SQLITE`: switches the project to SQLite for local development., set  to False if you want to use PostgreSQL.
- `ALLOWED_HOSTS`: comma-separated hosts allowed to serve the API.
- `CORS_ALLOWED_ORIGINS`: frontend origins allowed to call the backend.
- `CSRF_TRUSTED_ORIGINS`: trusted origins for CSRF protection.

## API Documentation

Swagger and schema endpoints are available through the configured API documentation setup.

Typical endpoints include:

- `/api/schema/`
- `/api/docs/`
- `/api/redoc/`

## Testing

Run the test suite with:

```bash
python manage.py test
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
