// https://nuxt.com/docs/api/configuration/nuxt-config
import Aura from "@primeuix/themes/aura";
import PrimeUI from "tailwindcss-primeui";
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: false },
  app: {
	head: {
	  title: "Nuxt App",
	},
	link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  }, 
  //srcDir: 'src/',  
  dir: {
    public: './public/'
  },  
  modules: [
    '@nuxt/content',
    '@nuxt/eslint',
    '@nuxt/fonts',
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/test-utils',
    '@nuxt/ui',
	'@nuxtjs/tailwindcss', 
	'@primevue/nuxt-module',
	'@tailwindcss/postcss',
	
    //'@pinia/nuxt',
    //'@vueuse/nuxt',
    //'@vite-pwa/nuxt',
    '@nuxtjs/google-fonts',
	
	'~/modules/primevue-sakai',
  ],
  
  typescript: {
    shim: false
  },  
  vite: {
	plugins: [
	  tailwindcss(),
	],
    build: {
      sourcemap: false
    },
    clearScreen: true,
    logLevel: 'info'	
  },
  primevue: {
    options: {
      theme: {
        preset: Aura,
          options: {
            darkModeSelector: ".p-dark",
          },
      },
      ripple: true,
    },
    autoImport: true,
  },
  nitro: {
    experimental: {
      asyncContext: true
    },

    future: {
      nativeSWR: true
    }
  },

  postcss: {
    plugins: {
      autoprefixer: {}
    }
  },

  imports: {
    autoImport: true,
    addons: {
      vueTemplate: true
    }
  },  
  build: {
    transpile: [
      'chart.js',
      'primevue'
    ]
  },
  components: {
    dirs: [
      {
        extensions: ['vue'],
        global: true,
        path: '~/components/common/',
        pathPrefix: false
      }
    ]
  },  
  
  css: [
    'primeicons/primeicons.css',
    //'~/assets/css/tailwind.css',
    //'primevue/resources/primevue.css',
    'primeflex/primeflex.css',
    'primeicons/primeicons.css',
    //'prismjs/themes/prism-coy.css',
    '~/assets/styles/layout.scss',
    '~/assets/demo/flags/flags.css',	
  ],
  tailwindcss: {
	exposeConfig: true,
    config: {
      plugins: [PrimeUI],
      darkMode: ["class", ".p-dark"],
    },
  },
  
  experimental: {
    asyncContext: true,
    headNext: true,
    typedPages: true,
    typescriptBundlerResolution: true
  },

  // @ts-ignore
  googleFonts: {
    families: {
      Inter: true
    }
  },  
})