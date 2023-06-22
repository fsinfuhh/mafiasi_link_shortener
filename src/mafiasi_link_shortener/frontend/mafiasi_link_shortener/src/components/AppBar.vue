<script setup lang="ts">
import { useAuthStore } from "@/stores";

const authStore = useAuthStore();

async function onLogoutClicked() {
  window.location.href = `${window.config.VITE_API_BASE as string}/auth/openid/logout/`;
}
</script>

<template>
  <v-app-bar>
    <template #prepend>
      <img src="@/assets/kurzlink.png" alt="Link Shortener Icon" width="40" height="40" />
    </template>
    <v-app-bar-title> Mafiasi Link Shortener </v-app-bar-title>
    <template #append>
      <v-btn class="mr-2" href="https://mafiasi.de/" prepend-icon="mdi-open-in-app">Mafiasi Dashboard</v-btn>
      <v-btn
        v-if="authStore.isAuthenticated"
        variant="flat"
        color="secondary"
        prepend-icon="mdi-logout"
        @click="onLogoutClicked"
        >Logout</v-btn
      >
    </template>
  </v-app-bar>
</template>

<style scoped>
#app-bar-icon svg {
  fill: black;
}
</style>
