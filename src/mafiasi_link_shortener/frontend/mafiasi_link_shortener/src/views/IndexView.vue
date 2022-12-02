<script setup lang="ts">
import { useAuthenticatedUser } from "@/auth";
import { useLinksApi } from "@/api";
import type { Link } from "@/api";
import { ref, watchEffect } from "vue";
import ShortlinkDetail from "@/components/ShortlinkDetail.vue";

const user = useAuthenticatedUser()!;
const linksApi = useLinksApi();

const links = ref<Link[]>([]);

async function refreshLinks(): Promise<void> {
  links.value = (await linksApi.value?.linksList())!.results!;
}

function onLinkDeleted(link: Link) {
  links.value = links.value.filter((i) => i !== link);
}

function onLinkUpdated(link: Link, newData: Partial<Link>) {
  Object.assign(link, newData);
}

watchEffect(async () => {
  if (linksApi.value != null) {
    await refreshLinks();
  }
});
</script>

<template>
  <div>
    <p v-if="user == null">Authenticating...</p>
    <p v-else-if="links === []">Loading...</p>
    <v-container v-else>
      <v-row>
        <v-col v-for="i_link in links" :key="i_link._short" :cols="4">
          <ShortlinkDetail :link="i_link" @deleted="onLinkDeleted(i_link)" @updated="onLinkUpdated(i_link, $event)" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<style scoped></style>
