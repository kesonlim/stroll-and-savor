/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        paper: {
          DEFAULT: '#F5F0E8',
          light: '#FAF7F2',
          card: '#FFFFFF',
          dark: '#E8E1D5',
        },
        ink: {
          DEFAULT: '#1A1A18',
          light: '#2D2D29',
          muted: '#686860',
          faint: '#9E9D93',
        },
        rust: {
          DEFAULT: '#C84B31',
          text: '#A63A22',
          dark: '#8C2E1A',
          subtle: '#FAEEEB',
        },
        teal: {
          DEFAULT: '#2D6E7E',
          text: '#205360',
          dark: '#183F49',
          subtle: '#E8F2F4',
        },
        rule: {
          DEFAULT: '#D8D2C5',
          light: '#EFECE6',
          dark: '#BCB5A4',
        },
        amber: {
          subtle: '#FEF8EC',
          border: '#E8B960',
        }
      },
      fontFamily: {
        sans: ['"IBM Plex Sans"', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"Space Mono"', 'monospace'],
        display: ['"Courier Prime"', 'Courier', 'serif'],
      },
      boxShadow: {
        'field': '0 2px 0 0 rgba(26,26,24,0.06), 0 8px 24px -4px rgba(26,26,24,0.08)',
        'stamp': '0 3px 0 0 #1A1A18',
        'stamp-rust': '0 3px 0 0 #C84B31',
        'stamp-teal': '0 3px 0 0 #2D6E7E',
      }
    },
  },
  plugins: [],
}
