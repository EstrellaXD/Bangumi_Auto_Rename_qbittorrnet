import { resolve } from 'node:path';
import UnoCSS from 'unocss/vite';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';
import VueRouter from 'unplugin-vue-router/vite';
import { VueRouterAutoImports } from 'unplugin-vue-router';
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite';
import { VitePWA } from 'vite-plugin-pwa';
import VueJsx from '@vitejs/plugin-vue-jsx';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  base: './',
  plugins: [
    VueJsx(),
    VueRouter({
      dts: 'types/dts/router-type.d.ts',
    }),
    vue({
      script: {
        defineModel: true,
      },
    }),
    UnoCSS(),
    AutoImport({
      imports: [
        'vue',
        'vitest',
        'pinia',
        '@vueuse/core',
        VueRouterAutoImports,
        'vue-i18n',
      ],
      dts: 'types/dts/auto-imports.d.ts',
      dirs: ['src/api', 'src/store', 'src/hooks', 'src/utils'],
    }),
    Components({
      dts: 'types/dts/components.d.ts',
      dirs: [
        'src/components',
        'src/components/basic',
        'src/components/layout',
        'src/components/setting',
      ],
    }),
    VueI18nPlugin({
      include: resolve(__dirname, './src/i18n/**'),
    }),
    VitePWA({
      injectRegister: false,
      registerType: 'autoUpdate',
      devOptions: {
        enabled: true,
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
      },
      manifest: {
        name: 'AutoBangumi',
        display: 'standalone',
        short_name: 'AutoBangumi',
        description: 'Automated Bangumi Download Tool',
        theme_color: '#ffffff',
        icons: [
          {
            src: '/images/logo.svg',
            sizes: 'any',
            type: 'image/svg+xml',
            purpose: 'any',
          },
          {
            src: '/images/pwa-192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: '/images/pwa-512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any',
          },
        ],
      },
    }),
  ],
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: '@import "./src/style/mixin.scss";',
      },
    },
  },
  esbuild: {
    drop: mode === 'production' ? ['console', 'debugger'] : [],
  },
  build: {
    cssCodeSplit: false,
  },
  resolve: {
    alias: {
      '~': resolve(__dirname, './'),
      '@': resolve(__dirname, 'src'),
      '#': resolve(__dirname, 'types'),
    },
  },
  server: {
    proxy: {
      '^/api/.*': 'http://192.168.0.100:7892',
      '^/posters/.*': 'http://192.168.0.100:7892',
    },
  },
}));
