<script setup lang="ts">
import type { Link } from "@/api";
import { useLinksApi } from "@/api";
import { ref } from "vue";
import ShortlinkEditForm from "@/components/EditShortlinkForm.vue";
import { useLinkStore } from "@/stores";

const props = defineProps<{
  link: Link;
}>();

const store = useLinkStore();

const linksApi = useLinksApi();

const isEditing = ref<boolean>(false);

async function onClickDelete(): Promise<void> {
  if (confirm(`Are you sure you want to delete shortlink ${props.link._short}?`)) {
    await linksApi.value!.linksDestroy({
      _short: props.link._short!,
    });
    store.delete(props.link._short!);
  }
}

function onClickCopy(): void {
  navigator.clipboard.writeText(props.link.shortlink).then(() => {});
}
</script>

<template>
  <!-- Normal display -->
  <v-card v-if="!isEditing">
    <v-card-title>
      <span>{{ props.link._short }}</span>
      <v-btn class="ml-1" icon="mdi-content-copy" variant="plain" size="small" @click="onClickCopy" />
    </v-card-title>
    <v-card-subtitle>{{ props.link.target }}</v-card-subtitle>
    <v-card-actions>
      <v-btn variant="outlined" :href="props.link.shortlink" target="_blank" prepend-icon="mdi-open-in-new"
        >Visit</v-btn
      >
      <v-btn color="primary" variant="outlined" prepend-icon="mdi-pencil" @click="isEditing = true">Edit</v-btn>
      <v-spacer />
      <v-btn color="red" variant="flat" prepend-icon="mdi-delete" @click="onClickDelete">Delete</v-btn>
    </v-card-actions>
  </v-card>

  <!-- Edit view -->
  <v-card v-else>
    <v-card-title>Edit {{ props.link._short }}</v-card-title>
    <ShortlinkEditForm :link="props.link" @updated="isEditing = false" @cancel="isEditing = false" />
  </v-card>
</template>

<style scoped></style>
