<script setup lang="ts">
import type { Link } from "@/api";
import type { VForm } from "vuetify/components";
import { useLinksApi } from "@/api";
import { reactive, ref } from "vue";

const props = defineProps<{
  link: Link;
}>();

const emit = defineEmits<{
  (e: "submit", linkData: Partial<Link>): void;
  (e: "cancel"): void;
}>();

const linksApi = useLinksApi();
const form = ref<VForm>();

const newData: Partial<Link> = reactive({
  target: props.link.target,
});

const targetValidationRules = [(v: string) => (!!v && v.length > 0) || "Target is required"];

async function onFormSubmit() {
  if ((await form.value!.validate()).valid) {
    emit("submit", newData);
  }
}
</script>

<template>
  <v-form ref="form" @submit.prevent="onFormSubmit">
    <v-container>
      <v-row>
        <!-- Target -->
        <v-col :cols="12">
          <v-text-field label="Target" v-model="newData.target" variant="underlined" :rules="targetValidationRules" />
        </v-col>
      </v-row>
    </v-container>

    <v-card-actions>
      <v-btn variant="outlined" prepend-icon="mdi-cancel" @click="emit('cancel')">Cancel</v-btn>
      <v-btn color="primary" variant="flat" prepend-icon="mdi-content-save" type="submit">Save</v-btn>
    </v-card-actions>
  </v-form>
</template>

<style scoped></style>
