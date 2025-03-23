import { tailwindConfig, createResolver, defineNuxtModule, addServerHandler, addTemplate } from 'nuxt/kit'
//exposeConfig: true
//import tailwindConfig from '#tailwind-config'
//import { theme } from '#tailwind-config'
//import screens from '#tailwind-config/theme/screens'  // default import
//import { _neutral } from '#tailwind-config/theme/colors'  // named (with _ prefix)
//import { _800 as slate800 } from '#tailwind-config/theme/colors/slate'  // alias

export default defineNuxtModule({
  setup (options, nuxt) {
    nuxt.hook('tailwindcss:config', function (tailwindConfig) {
      //tailwindConfig.theme.colors.blue = '#fff'
    })

    nuxt.hook('tailwindcss:resolvedConfig', function (resolvedConfig) {
      //console.log('This is the resulting config', JSON.stringify(resolvedConfig))
    })
  }
})

