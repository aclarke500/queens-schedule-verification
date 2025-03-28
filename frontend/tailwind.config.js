/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        queens: {
          red: '#CC0033',
          yellow: '#FFD700',
          blue: '#002D72'
        }
      }
    },
  },
  plugins: [],
}