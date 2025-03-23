<script lang="ts">
import { defineComponent } from 'vue';
import AppTopBar from '~/components/layouts/default/AppTopbar.vue';
import AppMenu from '~/components/layouts/default/AppMenu.vue';
import AppConfig from '~/components/layouts/default/AppConfig.vue';
import AppFooter from '~/components/layouts/default/AppFooter.vue';

export default defineComponent({
  components: {
    AppTopBar,
    AppMenu,
    AppConfig,
    AppFooter
  },
  data() {
    return {
      layoutMode: 'static',
      menuActive: false,
      menuClick: false,
      staticMenuInactive: false,
      overlayMenuActive: false,
      mobileMenuActive: false,
      menu: [
        {
          label: 'Школа лётных искусств',
          items: [{
            label: 'Главная', icon: 'pi pi-fw pi-home', to: '/'
          }]
        },
        {
          label: 'Разделы',
          icon: 'pi pi-fw pi-sitemap',
          items: [
            { label: 'О курсах', icon: 'pi pi-fw pi-id-card', to: '/about' },
            { label: 'Профиль', icon: 'pi pi-fw pi-check-square', to: '/profile' },
            { label: 'Наши услуги', icon: 'pi pi-fw pi-bookmark', to: '/services' },			
            { label: 'Прайс', icon: 'pi pi-fw pi-bookmark', to: '/price' },
            { label: 'Обучение', icon: 'pi pi-fw pi-exclamation-circle', to: '/courses' },
            { label: 'Переподготовка', icon: 'pi pi-fw pi-mobile', to: '/dpo' },
            { label: 'Симулятор тренажёра', icon: 'pi pi-fw pi-table', to: '/sims' },
          ]
        },
        {
          label: 'Круг общения',
          icon: 'pi pi-fw pi-sitemap',
          items: [
            { label: 'Мои друзья', icon: 'pi pi-fw pi-id-card', to: '/demo/formlayout' },
            { label: 'Преподаватели', icon: 'pi pi-fw pi-check-square', to: '/demo/input' },
            { label: 'Желаемые Рейсы', icon: 'pi pi-fw pi-bookmark', to: '/demo/floatlabel2' },			
          ]
        },		
        {
          label: 'Курсы подготовки',
          icon: 'pi pi-fw pi-search',
          items: [
            {
              label: 'Общие Курсы',
              icon: 'pi pi-fw pi-bookmark',
              items: [
                {
                  label: 'Для новичков',
                  icon: 'pi pi-fw pi-bookmark',
                  items: [
                    { label: 'Submenu 1.1.1', icon: 'pi pi-fw pi-bookmark' },
                    { label: 'Submenu 1.1.2', icon: 'pi pi-fw pi-bookmark' },
                    { label: 'Submenu 1.1.3', icon: 'pi pi-fw pi-bookmark' }
                  ]
                },
              ]
            },
          ]
        },
        {
          label: 'Помощь',
          items: [
		    { label: 'Лицензии', icon: 'pi pi-fw pi-circle-off', to: '/demo/misc' },
            {
              label: 'Поддержка',
              icon: 'pi pi-fw pi-question',
              command: () => {
                window.location.href = '/documentation';
              }
            },
            { label: 'На сайт s7', icon: 'pi pi-fw pi-search', url: 'https://s7.ru' }
          ]
        }
      ]
    };
  },
  computed: {
    containerClass() {
      return ['layout-wrapper', {
        'layout-overlay': this.layoutMode === 'overlay',
        'layout-static': this.layoutMode === 'static',
        'layout-static-sidebar-inactive': this.staticMenuInactive && this.layoutMode === 'static',
        'layout-overlay-sidebar-active': this.overlayMenuActive && this.layoutMode === 'overlay',
        'layout-mobile-sidebar-active': this.mobileMenuActive,
        'p-input-filled': this.$primevue.config.inputStyle === 'filled',
        'p-ripple-disabled': this.$primevue.config.ripple === false,
        'layout-theme-light': this.$appState.theme?.startsWith('saga')
      }];
    },
    logo() {
      return (this.$appState.darkTheme) ? '/images/logo-white.svg' : '/images/logo.svg';
    }
  },
  watch: {
    $route() {
      this.menuActive = false;
      this.$toast.removeAllGroups();
    }
  },
  beforeUpdate() {
    if (this.mobileMenuActive) {
      this.addClass(document.body, 'body-overflow-hidden');
    } else {
      this.removeClass(document.body, 'body-overflow-hidden');
    }
  },
  methods: {
    onWrapperClick() {
      if (!this.menuClick) {
        this.overlayMenuActive = false;
        this.mobileMenuActive = false;
      }

      this.menuClick = false;
    },
    onMenuToggle(event: Event) {
      this.menuClick = true;

      if (this.isDesktop()) {
        if (this.layoutMode === 'overlay') {
          if (this.mobileMenuActive) {
            this.overlayMenuActive = true;
          }

          this.overlayMenuActive = !this.overlayMenuActive;
          this.mobileMenuActive = false;
        } else if (this.layoutMode === 'static') {
          this.staticMenuInactive = !this.staticMenuInactive;
        }
      } else {
        this.mobileMenuActive = !this.mobileMenuActive;
      }

      event.preventDefault();
    },
    onSidebarClick() {
      this.menuClick = true;
    },
    onMenuItemClick(event: any) {
      if (event.item && !event.item.items) {
        this.overlayMenuActive = false;
        this.mobileMenuActive = false;
      }
    },
    onLayoutChange(layoutMode: string) {
      this.layoutMode = layoutMode;
    },
    addClass(element: Element, className: string) {
      if (element.classList) {
        element.classList.add(className);
      } else {
        element.className += ` ${className}`;
      }
    },
    removeClass(element: Element, className: string) {
      if (element.classList) {
        element.classList.remove(className);
      } else {
        element.className = element.className.replace(new RegExp(`(^|\\b)${className.split(' ').join('|')}(\\b|$)`, 'gi'), ' ');
      }
    },
    isDesktop() {
      return window.innerWidth >= 992;
    },
    isSidebarVisible() {
      if (this.isDesktop()) {
        if (this.layoutMode === 'static') {
          return !this.staticMenuInactive;
        } else if (this.layoutMode === 'overlay') {
          return this.overlayMenuActive;
        }
      }

      return true;
    }
  }
});
</script>

<template>
  <div :class="containerClass" @click="onWrapperClick">
    <AppTopBar @menu-toggle="onMenuToggle" />
    <div class="layout-sidebar" @click="onSidebarClick">
      <AppMenu :model="menu" @menuitem-click="onMenuItemClick" />
    </div>

    <div class="layout-main-container">
      <div class="layout-main">
        <slot />
      </div>
      <AppFooter />
    </div>

    <AppConfig :layout-mode="layoutMode" @layout-change="onLayoutChange" />
    <transition name="layout-mask">
      <div v-if="mobileMenuActive" class="layout-mask p-component-overlay" />
    </transition>
  </div>
</template>

<style lang="scss">
  @use '~/assets/styles/App.scss';
</style>
