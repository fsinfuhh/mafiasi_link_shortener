import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import runtimeConfig from "vite-plugin-runtime-config";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), runtimeConfig()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
