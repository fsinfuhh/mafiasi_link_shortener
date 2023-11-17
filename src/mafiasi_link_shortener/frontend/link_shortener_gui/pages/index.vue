<script setup lang="ts">
definePageMeta({
  middleware: ["authenticated"],
})

const api = await useLinksApi();

const links = await api.linksList();
</script>

<template>
  <UContainer>
    <h1>{{ links }}</h1>
  </UContainer>
</template>
