import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "APEX TERMINAL // Next-Gen AI Bloomberg",
  description: "Autonomous Multi-Agent Financial Intelligence Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-[#08090d] text-[#e0e6ed] select-none">
        {children}
      </body>
    </html>
  );
}
