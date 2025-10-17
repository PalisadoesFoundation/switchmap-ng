import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "next-themes";
import Footer from "./components/Footer";

/**
 * RootLayout component that wraps the entire application.
 *
 * @remarks
 * This component sets up the HTML structure, including the `<html>` and `<body>` tags.
 * It integrates the `next-themes` library to provide theme switching capabilities
 * and applies global fonts using the `next/font` package. The layout also includes
 * a footer component for consistent page structure.
 *
 * @returns The root layout component.
 *
 * @see {@link ThemeProvider} from `next-themes` for theme management.
 * @see {@link Geist} and {@link Geist_Mono} from `next/font/google` for font integration.
 * @see {@link Footer} for the footer component displayed on all pages.
 *
 */

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Switchmap-NG",
  description: "A Modern Network Monitoring and Analysis Tool",
  icons: {
    icon: "/images/switchmap-logo-modified.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  );
}
