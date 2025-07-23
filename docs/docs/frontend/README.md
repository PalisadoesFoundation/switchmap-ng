**frontend**

***

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

# SwitchMap-NG Frontend

This folder contains the modern frontend for SwitchMap-NG, responsible for rendering network dashboards, visualizations, and device data.

## Getting Started

Make sure the backend server is running before starting the frontend.

1. **Install dependencies:**

```bash
npm install

```
2. **Start the development server:**

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

## Directory Structure
<pre> ``` frontend/ ├── .next/ # Next.js build output (auto-generated) ├── node_modules/ # Installed dependencies ├── src/ │ └── app/ │ ├── components/ # UI components │ ├── devices/ # Device-related pages and components │ ├── globals.css # Global styles and theming │ ├── layout.tsx # Root layout component │ ├── page.tsx # Main entry page │ └── theme-toggle.tsx # Theme toggle component ├── .env.local # Local environment variables (gitignored) ├── package.json # Project metadata and scripts ├── next.config.ts # Next.js configuration ├── tsconfig.json # TypeScript configuration ├── tailwind.config.js # Tailwind CSS configuration ├── postcss.config.mjs # PostCSS configuration ├── README.md # Frontend-specific documentation ``` </pre>
