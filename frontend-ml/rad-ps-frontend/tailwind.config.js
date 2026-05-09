/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#131314', // Deep dark for main background
        card: '#1e1e20',       // Darker gray for cards
        cardHover: '#2a2a2d',
        accent: '#4ade80',     // Vibrant green
        accentHover: '#22c55e',
        textPrimary: '#f3f4f6',
        textSecondary: '#9ca3af',
        danger: '#ef4444',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
