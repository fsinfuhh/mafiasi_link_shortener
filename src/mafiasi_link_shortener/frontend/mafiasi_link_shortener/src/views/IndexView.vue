<script setup lang="ts">
import { useAuthenticatedUser } from "@/auth";
import { watchEffect } from "vue";

const user = useAuthenticatedUser();

watchEffect(() => {
  console.log(user.value);
});
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
