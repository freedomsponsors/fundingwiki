import { defineConfig, loadEnv } from 'vite'
import { fileURLToPath, URL } from 'node:url'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const isMock = (env.VITE_MOCK ?? process.env.VITE_MOCK) === 'true'

  console.log('isMock', isMock)

  return {
    plugins: [vue()],
    resolve: {
      alias: [
        ...(isMock ? [
          { find: '@/services/ideas.js', replacement: fileURLToPath(new URL('./src/services/ideas.mock.js', import.meta.url)) },
          { find: '@/services/user.js', replacement: fileURLToPath(new URL('./src/services/user.mock.js', import.meta.url)) },
        ] : []),
        { find: '@', replacement: fileURLToPath(new URL('./src', import.meta.url)) },
      ],
    },
    server: {
      proxy: {
        '/login': 'http://localhost:8000',
        '/logout': 'http://localhost:8000',
        '/accounts': 'http://localhost:8000',
        '/admin': 'http://localhost:8000',
        '/static': 'http://localhost:8000',
        '/vueapi': 'http://localhost:8000',
      },
    },
  }
})
