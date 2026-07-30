# Selora Shop Frontend

Selora Frontend is the customer-facing web application for the Selora Shop e-commerce platform. It is built with Next.js and provides a polished shopping experience with landing pages, product browsing, authentication, cart management, and user account flows.

## Overview

This frontend connects to the Selora backend API and is designed for:

- product discovery and browsing
- user registration and login
- cart and checkout-related interactions
- responsive, modern UI with reusable components
- fast development with a feature-based architecture

## Tech Stack

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS
- shadcn/ui and Radix UI primitives
- Framer Motion
- React Hook Form + Zod
- TanStack React Query
- Zustand
- Sonner for toast notifications
- Lucide React icons

## Project Structure

```text
selora-frontend/
├── app/                  # App Router pages and layouts
│   ├── auth/             # Authentication-related routes
│   ├── cart/             # Cart pages
│   ├── panel/            # User/admin panel routes
│   ├── products/         # Product-related routes
│   └── page.tsx          # Landing page
├── components/           # Shared UI and page-level components
│   ├── layouts/          # Header, footer, layout wrappers
│   ├── pages/            # Landing page sections
│   └── ui/               # Reusable UI primitives
├── features/             # Feature modules
│   ├── api/              # API client and response types
│   ├── auth/             # Auth actions, hooks, and state
│   ├── cart/             # Cart logic and actions
│   ├── preferences/      # User preferences
│   ├── shared/           # Shared feature utilities
│   ├── store/            # Store-related logic
│   └── user/             # User profile features
├── public/               # Static assets and PWA files
├── next.config.ts        # Next.js config and image remote patterns
└── package.json          # Scripts and dependencies
```

## Main Features

- responsive landing page with hero, product highlights, and CTA sections
- auth flow for sign-in and sign-out
- cart state handling with persistent client-side actions
- modular UI built with reusable components
- support for serving backend media files through Next.js image config

## Requirements

Make sure the following are installed:

- Node.js 20+
- npm 10+

Verify your environment:

```bash
node -v
npm -v
```

## Getting Started

1. Install dependencies:

```bash
cd selora-frontend
npm install
```

2. Configure environment variables:

Copy the example file and adjust the backend URL if needed:

```bash
cp .env.example .env
```

Example values:

```env
BASE_API_URL="http://127.0.0.1:8000/api/v1/"
NEXT_PUBLIC_BASE_API_URL="http://127.0.0.1:8000/api/v1/"
```

3. Start the development server:

```bash
npm run dev
```

Open http://localhost:3000 in your browser.

## Available Scripts

```bash
npm run dev      # start the development server
npm run build    # create a production build
npm run start    # start the production server
npm run lint     # run ESLint
```

## Run with Docker

Build and start the frontend container:

```bash
docker build -t selora-frontend .
docker run -p 3000:3000 selora-frontend
```

You can also use Docker Compose from the project root:

```bash
docker compose up frontend --build
```

## Backend Connection

The frontend expects the Selora backend to be running and reachable at the configured API base URL. The default setup points to:

```text
http://127.0.0.1:8000/api/v1/
```

## Environment Variables

Create a `.env` file in the frontend folder and set the values you need:

```env
BASE_API_URL="http://127.0.0.1:8000/api/v1/"
NEXT_PUBLIC_BASE_API_URL="http://127.0.0.1:8000/api/v1/"
```

### Variables

- `BASE_API_URL`: base URL used by internal server-side configuration.
- `NEXT_PUBLIC_BASE_API_URL`: public API URL exposed to the browser and used by client-side requests.

## Notes

- The app uses a standalone Next.js output configuration.
- Image optimization is configured for backend media paths.
- The project follows a feature-based structure to keep auth, cart, and shared UI concerns organized.

```tsx
import { Button } from "@/components/ui/button";

export function Example() {
    return (
        <Button>
            Add to cart
        </Button>
    );
}
```

---

# 🌐 API Layer

All API communication is handled through Axios.

Structure:

```
services
│
└── api.ts
```

Example:

```ts
export const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
});
```

---

# 🔄 React Query

Server state management uses TanStack Query.

Example:

```ts
const {
    data,
    isLoading,
} = useQuery({
    queryKey: ["products"],
    queryFn: getProducts,
});
```

Benefits:

- Automatic caching
- Background refetching
- Loading states
- Error handling

---

# 📝 Form Handling

Forms use:

- React Hook Form
- Zod validation


Example:

```ts
const schema = z.object({
    email: z.string().email(),
});
```

---

# 🔒 Authentication

Authentication flow:

```
User
 |
 |
Login
 |
 |
API
 |
 |
JWT Token
 |
 |
HttpOnly Cookie
 |
 |
Authenticated Requests
```

Features:

- Secure cookie storage
- Protected routes
- Session handling

---

# 🛒 Store Features

Implemented:

- Product listing
- Product details
- Categories
- Product variants
- Variant attributes
- Product images
- Stock status

---

# 🛍 Cart Features

Implemented:

- Add product to cart
- Update quantity
- Remove item
- Persistent cart session
- Stock validation

---


# 🧪 Testing

Run tests:

```bash
npm run test
```

---

# 📌 Code Style

Rules:

- TypeScript strict mode
- No implicit any
- Functional components
- Feature-based structure
- Reusable components
- Typed API responses

---

# 🔥 Performance

Implemented optimizations:

- Server Components
- Dynamic imports
- React Query caching
- Image optimization
- Component lazy loading
- Memoization where required

---

# 🚀 Deployment

Recommended:

- Vercel
- Docker
- Node.js server


Build:

```bash
npm run build
```

Start:

```bash
npm run start
```

---

# 🤝 Contribution

Before submitting changes:

1. Run lint

```bash
npm run lint
```

2. Check TypeScript

```bash
npm run type-check
```

3. Test build

```bash
npm run build
```

---

# 📄 License

Private project.

All rights reserved.

---

# 👨‍💻 Author

Pouria Darandi
```