/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://your-replit-backend-url.repl.co'
  },
  // Required for Replit deployment
  output: 'standalone'
}

module.exports = nextConfig
