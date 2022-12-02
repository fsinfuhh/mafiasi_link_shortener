import { createApp } from "vue";
import App from "./App.vue";

// vuetify
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { createPinia } from "pinia";

const vuetify = createVuetify({
  components,
  directives,
});

// pinia
const pinia = createPinia();

createApp(App).use(vuetify).use(pinia).mount("#app");
