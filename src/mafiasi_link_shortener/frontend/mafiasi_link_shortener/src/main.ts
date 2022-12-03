import { createApp } from "vue";
import App from "./App.vue";

// vuetify
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import { createVuetify } from "vuetify";
import { createPinia } from "pinia";
const vuetify = createVuetify();

// pinia
const pinia = createPinia();

createApp(App).use(vuetify).use(pinia).mount("#app");
