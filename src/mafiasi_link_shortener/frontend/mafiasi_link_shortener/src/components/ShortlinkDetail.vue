<script setup lang="ts">
import type { Link } from "@/api";
import { useLinksApi } from "@/api";

const props = defineProps<{
  link: Link;
}>();

const emit = defineEmits<{
  (e: "deleted"): void;
}>();

const linksApi = useLinksApi();

async function onClickDelete(): Promise<void> {
  if (confirm(`Are you sure you want to delete shortlink ${props.link._short}?`)) {
    await linksApi.value?.linksDestroy({
      _short: props.link._short!,
    });
    emit("deleted");
  }
}
</script>

<template>
  <v-card>
    <v-card-title>{{ props.link._short }}</v-card-title>
    <v-card-subtitle
      ><i>{{ props.link.target }}</i></v-card-subtitle
    >
    <v-card-actions>
      <v-btn variant="outlined" :href="props.link.target">Visit</v-btn>
      <v-spacer />
      <v-btn color="red" variant="flat" prepend-icon="mdi-delete" @click="onClickDelete">Delete</v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped></style>
