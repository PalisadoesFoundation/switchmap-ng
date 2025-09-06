import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "next-themes";

/**
 * Root layout for the application.
 * This component sets up global styles and the theme provider.
 * It uses the Geist and Geist Mono fonts from Google Fonts.
 * The layout wraps the entire application and provides a consistent theme
 * across all pages.
 *
 * @remarks
 * The `ThemeProvider` manages the theme state,
 * allowing users to switch between light and dark modes.
 * The `metadata` object defines the application's title and description.
 * `RootLayout` is the main entry point for the app layout,
 * ensuring fonts are applied globally and theme is set correctly.
 *
 * @returns The rendered component.
 *
 * @see {@link ThemeProvider} for managing themes in Next.js.
 * @see {@link Geist} and {@link Geist_Mono} for the fonts used in the layout.
 * @see {@link Metadata} for defining the page metadata.
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
        </ThemeProvider>
      </body>
    </html>
  );
}
