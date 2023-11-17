// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    extends: ["nuxt_layer_mafiasi"],
    app: {
        baseURL: "/app",
    },
    runtimeConfig: {
        public: {
            apiBase: ""
        }
    }
})
