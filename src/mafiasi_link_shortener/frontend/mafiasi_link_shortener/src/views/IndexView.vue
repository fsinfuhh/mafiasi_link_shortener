<script setup lang="ts">
import { useAuthenticatedUser } from "@/auth";

const user = useAuthenticatedUser();
</script>

<template>
  <div>
    <p v-if="user == null">Authenticating...</p>
    <div v-else>
      <p>Hello {{ user.profile.sub }}</p>
    </div>
  </div>
</template>

<style scoped></style>
