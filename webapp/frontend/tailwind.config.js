/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        fair: {
          f: '#3B82F6',
          a: '#10B981',
          i: '#8B5CF6',
          r: '#F59E0B',
        },
      },
    },
  },
  plugins: [],
}
