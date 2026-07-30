# Selora Shop

Selora Shop is a full-stack e-commerce project with a Django REST backend and a Next.js frontend.

## What this project includes

- a modern storefront UI for browsing products
- authentication and user-related flows
- cart interactions connected to the backend API
- a modular structure for frontend and backend development

## Project structure

```text
selora-shop/
├── selora-backend/   # Django REST API
├── selora-frontend/  # Next.js app
└── README.md         # project overview
```

## Tech stack

- Backend: Django, Django REST Framework, JWT auth
- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Tools: ESLint, pytest, and modern UI components

## Quick start

### Backend

```bash
cd selora-backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd selora-frontend
npm install
npm run dev
```

## Documentation

- Backend docs: [selora-backend/README.md](selora-backend/README.md)
- Frontend docs: [selora-frontend/README.md](selora-frontend/README.md)

## Notes

This repository is organized as a monorepo with separate backend and frontend apps, making it easier to develop and maintain each part independently.
