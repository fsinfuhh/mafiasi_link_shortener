<script setup lang="ts">
import { useLinksApi } from "@/api";
import { watchEffect } from "vue";
import ShortlinkDetail from "@/components/ShortlinkDetail.vue";
import { useAuthStore, useLinkStore } from "@/stores";

const authStore = useAuthStore();
const linkStore = useLinkStore();
const linksApi = useLinksApi();

// fetch links as soon as an API client is available
watchEffect(async () => {
  if (linksApi.value != null && linkStore.links.length === 0) {
    linkStore.links = (await linksApi.value?.linksList())!.results!;
  }
});
</script>

<template>
  <div>
    <p v-if="!authStore.isAuthenticated">Authenticating...</p>
    <p v-else-if="linkStore.links === []">Loading...</p>
    <v-container v-else>
      <v-row>
        <v-col v-for="i_link in linkStore.links" :key="i_link._short" :cols="4">
          <ShortlinkDetail :link="i_link" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<style scoped></style>
