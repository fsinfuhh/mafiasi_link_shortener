<script setup lang="ts">
import type { Link, ResponseError } from "@/api";
import type { VForm } from "vuetify/components";
import type { Ref } from "vue";
import { reactive, ref } from "vue";
import { useLinkStore } from "@/stores";
import { useLinksApi } from "@/api";

const props = defineProps<{
  link: Link;
}>();

const emit = defineEmits<{
  (e: "updated", newLinkData: Link): void;
  (e: "cancel"): void;
}>();

const store = useLinkStore();
const api = useLinksApi();
const form = ref<VForm>();

const newData: Partial<Link> = reactive({
  target: props.link.target,
});
const apiErrors: Ref<Record<string, string[]>> = ref({});

async function onFormSubmit() {
  if ((await form.value!.validate()).valid) {
    try {
      const newLink = await api.value!.linksPartialUpdate({
        _short: props.link._short!,
        patchedLinkRequest: newData,
      });
      store.update(props.link._short!, newLink);
      emit("updated", newLink);
    } catch (e) {
      const error = e as ResponseError;
      apiErrors.value = await error.response.json();
    }
  }
}
</script>

<template>
  <v-form ref="form" @submit.prevent="onFormSubmit">
    <v-container>
      <v-row>
        <!-- Target Form-Field -->
        <v-col :cols="12">
          <v-text-field
            id="target"
            label="Destination"
            hint="Where the shortlink leads"
            placeholder="https://example.com/"
            v-model="newData.target"
            variant="underlined"
            :error-messages="apiErrors['target']"
            @update:modelValue="apiErrors['target'] = []"
          />
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
