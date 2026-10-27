// @ts-check
import { defineConfig } from 'astro/config';

import react from '@astrojs/react';

const faceApiProxy = {
  '/api/v1/face/annotate': {
    target: 'https://backend-tau-seven-48jsbet9kg.vercel.app',
    changeOrigin: true,
  },
};

// https://astro.build/config
export default defineConfig({
  integrations: [react()],
  vite: {
    optimizeDeps: {
      force: true,
    },
    server: {
      proxy: faceApiProxy,
    },
    preview: {
      proxy: faceApiProxy,
    },
  },
});