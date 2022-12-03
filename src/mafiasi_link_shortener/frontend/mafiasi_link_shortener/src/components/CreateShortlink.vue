<script setup lang="ts">
import CreateShortlinkForm from "@/components/CreateShortlinkForm.vue";
import type { Link, LinkRequest } from "@/api";
import { useLinksApi } from "@/api";
import { useLinkStore } from "@/stores";

const emit = defineEmits<{
  (e: "close"): void;
}>();

const api = useLinksApi();
const store = useLinkStore();

async function onFormSubmit(linkData: LinkRequest) {
  const link = await api.value!.linksCreate({
    linkRequest: linkData,
  });
  store.add(link);
  emit("close");
}
</script>

<template>
  <v-card>
    <v-card-title>Create New Shortlink</v-card-title>
    <CreateShortlinkForm @submit="onFormSubmit" @cancel="emit('close')" />
  </v-card>
</template>

<style scoped></style>
