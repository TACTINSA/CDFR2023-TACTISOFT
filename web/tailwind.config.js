/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'class', content: ["./src/**/*.njk", "./src/**/*.svg"], theme: {
        extend: {},
    }, plugins: [require('flowbite/plugin')]
}
