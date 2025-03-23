/** @type {import('tailwindcss').Config} */
import type { Config } from 'tailwindcss';
import colors from 'tailwindcss/colors'
import PrimeUI from 'tailwindcss-primeui';

export default <Partial<Config>>{
  content: [],
  theme: {
    extend: {
      colors: {
		primary: colors.green
	  }
	},
  },
  darkMode: ['selector', '[class~="my-app-dark"]'], 
  plugins: [
    PrimeUI,
    '@tailwindcss/postcss',
  ],
}

