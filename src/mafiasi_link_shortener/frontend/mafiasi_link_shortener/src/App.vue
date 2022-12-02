<script setup lang="ts">
import IndexView from "@/views/IndexView.vue";
import { createUserManager, USER_MANGER_SYMBOL } from "@/auth";
import { provide } from "vue";

const userManager = createUserManager();
provide(USER_MANGER_SYMBOL, userManager);
</script>

<template>
  <header>
    <h1>Mafiasi Link Shortener</h1>
  </header>

  <main>
    <IndexView />
  </main>
</template>

<style scoped></style>
