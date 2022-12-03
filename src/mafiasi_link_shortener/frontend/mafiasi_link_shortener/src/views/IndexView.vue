<script setup lang="ts">
import { useLinksApi } from "@/api";
import { ref, watchEffect } from "vue";
import ShortlinkDetail from "@/components/ShortlinkDetail.vue";
import { useAuthStore, useLinkStore } from "@/stores";
import CreateShortlinkForm from "@/components/CreateShortlinkForm.vue";
import CreateShortlink from "@/components/CreateShortlink.vue";

const authStore = useAuthStore();
const linkStore = useLinkStore();
const linksApi = useLinksApi();

const isCreatePopupOpen = ref(false);

// fetch links as soon as an API client is available
watchEffect(async () => {
  if (linksApi.value != null && linkStore.links.length === 0) {
    linkStore.links = (await linksApi.value?.linksList())!.results!;
  }
});
</script>

<template>
  <div>
    <!-- Loading states -->
    <p v-if="!authStore.isAuthenticated">Authenticating...</p>
    <p v-else-if="linkStore.links === []">Loading...</p>

    <!-- Main content -->
    <v-container v-else>
      <v-row>
        <!-- Link Detail List -->
        <v-col v-for="i_link in linkStore.links" :key="i_link._short" :cols="4">
          <ShortlinkDetail :link="i_link" />
        </v-col>
      </v-row>

      <!-- New Link Creation -->
      <v-dialog v-model="isCreatePopupOpen">
        <template #activator="{ props }">
          <v-btn id="btn-add" icon="mdi-plus" color="primary" size="x-large" v-bind="props" />
        </template>
        <CreateShortlink @close="isCreatePopupOpen = false" />
      </v-dialog>
    </v-container>
  </div>
</template>

<style scoped>
#btn-add {
  z-index: 10;
  position: fixed;
  bottom: 28px;
  right: 32px;
}
</style>
