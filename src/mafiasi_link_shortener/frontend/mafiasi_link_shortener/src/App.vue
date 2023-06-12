<script setup lang="ts">
import IndexView from "@/views/IndexView.vue";
import { onMounted } from "vue";
import { useAuthStore } from "@/stores";
import AppBar from "@/components/AppBar.vue";

const authStore = useAuthStore();
onMounted(async () => {
  await fetch(`${window.config.VITE_API_BASE as string}/api/logged_in/`, {
    credentials: "include",
  })
    .then((response) => {
      console.log(response);
      if (response.status === 200) {
        authStore.isAuthenticated = true;
      } else {
        authStore.isAuthenticated = false;
        window.location.href = `${window.config.VITE_API_BASE as string}/auth/openid/login/`;
      }
    })
    .catch((error) => {
      console.log(error);
      authStore.isAuthenticated = false;
      window.location.href = `${window.config.VITE_API_BASE as string}/auth/openid/login/`;
    });
  console.log(authStore.isAuthenticated);
});

const SWAGGER_URL = `${window.config.VITE_API_BASE as string}/api/schema/swagger-ui/`;
</script>

<template>
  <v-app>
    <AppBar />

    <!-- Main Content -->
    <v-main>
      <IndexView />
    </v-main>

    <!-- footer -->
    <v-footer class="d-flex justify-center flex-grow-0">
      <v-btn
        class="mx-4"
        variant="flat"
        prepend-icon="mdi-github"
        href="https://github.com/fsinfuhh/mafiasi_link_shortener"
      >
        Source Code
      </v-btn>
      <v-btn class="mx-4" variant="flat" prepend-icon="mdi-console-network" :href="SWAGGER_URL"> API</v-btn>
    </v-footer>
  </v-app>
</template>

<style scoped></style>
