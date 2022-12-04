<script setup lang="ts">
import { inject } from "vue";
import { USER_MANGER_SYMBOL } from "@/auth";
import type { UserManager } from "oidc-client-ts";
import { useAuthStore } from "@/stores";

const authStore = useAuthStore();
const userManager = inject<UserManager>(USER_MANGER_SYMBOL)!;

async function onLogoutClicked() {
  await userManager.removeUser();
  await userManager.signoutRedirect({
    post_logout_redirect_uri: "https://mafiasi.de/",
  });
}
</script>

<template>
  <v-app-bar>
    <template #prepend>
      <img src="@/assets/favicon.ico" alt="Link Shortener Icon" width="50" height="50" />
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
