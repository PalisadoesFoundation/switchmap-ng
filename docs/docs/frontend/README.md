**frontend**

***

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

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

frontend/
├── .next/ # Next.js build output (auto-generated)
├── node_modules/ # Installed dependencies
├── src/
│ └── app/
│ ├── components/ # UI components
│ ├── devices/ # Device-related pages and components
│ ├── globals.css # Global styles and theming
│ ├── layout.tsx # Root layout component
│ ├── page.tsx # Main entry page
│ └── theme-toggle.tsx # Theme toggle component
├── .env.local # Local environment variables (gitignored)
├── package.json # Project metadata and scripts
├── next.config.ts # Next.js configuration
├── tsconfig.json # TypeScript configuration
├── tailwind.config.js # Tailwind CSS configuration
├── postcss.config.mjs # PostCSS configuration
├── README.md # Frontend-specific documentation
