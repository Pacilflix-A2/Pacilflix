/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Add the paths to your HTML files here
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      fontFamily: {
        lexend: ["Lexend", "sans-serif"],
      },
    },
  },
  plugins: [],
};
