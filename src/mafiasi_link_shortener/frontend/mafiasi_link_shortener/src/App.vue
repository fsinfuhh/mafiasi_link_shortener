<script setup lang="ts">
import IndexView from "@/views/IndexView.vue";
import { createUserManager, getUserOrLogin, USER_MANGER_SYMBOL, AUTHENTICATED_USER_SYMBOL } from "@/auth";
import { onMounted, provide, ref } from "vue";

const userManager = createUserManager();
provide(USER_MANGER_SYMBOL, userManager);

const user = ref();
provide(AUTHENTICATED_USER_SYMBOL, user);
onMounted(async () => {
  user.value = await getUserOrLogin(userManager);
});

const SWAGGER_URL = `${window.config.VITE_API_BASE as string}/api/schema/swagger-ui/`;
</script>

<template>
  <v-app>
    <!-- Top Bar -->
    <v-app-bar title="Mafiasi Link Shortener" />

    <!-- Main Content -->
    <v-main>
      <IndexView />
    </v-main>

    <!-- footer -->
    <v-footer class="d-flex justify-center">
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
