**frontend**

***

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

# SwitchMap-NG Frontend

This folder contains the modern frontend for SwitchMap-NG, responsible for rendering network dashboards, visualizations, and device data.

## Getting Started

> **Make sure the backend API server is running before starting the frontend.**  
> Refer to the [Installation Guide](/docs/installation) for backend setup instructions.
> Set up the pre-commit hook to automatically generate documentation when committing changes:

```bash
python scripts/setup_hooks.py

```
1. **Navigate to the frontend directory:**
```bash
cd frontend

```

2. **Install dependencies:**

```bash
npm install

```
3. **Start the development server:**

```bash
npm run dev

```
The frontend will be available at http://localhost:3000.

## Project Overview

This frontend interfaces with the SwitchMap-NG backend (Flask + GraphQL) to present real-time network data. Features include:

- Device and port dashboards
- Network topology visualization
- Theme-aware UI with dark/light modes
- Charts for bandwidth, CPU, memory, and uptime

## Tech Stack
- Next.js 15.3.3 (App Router)
- React 19
- Tailwind CSS 4
- TypeScript
- Theming using CSS custom properties and next-themes
- Fetch API for backend GraphQL communication

### Directory Structure

```txt
frontend/
├── src/
│   └── app/
│       ├── components/         # UI components
│       ├── devices/            # Device-specific pages
│       ├── globals.css         # Global styles
│       ├── layout.tsx          # Root layout
│       ├── page.tsx            # Main entry page
│       └── theme-toggle.tsx    # Theme toggle
│   └── types/                  # Shared TypeScript types
├── .env.local                  # Environment variables (not committed)
├── .gitignore
├── next.config.ts              # Next.js config
├── tsconfig.json               # TypeScript config
├── typedoc.json                # Typedoc config
├── postcss.config.mjs          # PostCSS config
├── eslint.config.mjs           # ESLint config
├── package.json                # Project metadata and scripts
├── package-lock.json
└── README.md                   # Frontend Read Me file
```
