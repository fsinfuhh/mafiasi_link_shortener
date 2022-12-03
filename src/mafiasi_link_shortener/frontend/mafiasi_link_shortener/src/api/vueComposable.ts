import type { Ref } from "vue";
import { LinksApi } from "@/api/apis";
import { computed } from "vue";
import { Configuration } from "@/api/runtime";
import { useAuthStore } from "@/stores";

export function useLinksApi(): Ref<LinksApi | null> {
  const authStore = useAuthStore();

  return computed(() => {
    if (authStore.currentUser == null) {
      return null;
    }

    return new LinksApi(
      new Configuration({
        basePath: window.config.VITE_API_BASE as string,
        headers: {
          Authorization: `Bearer ${authStore.currentUser.access_token}`,
        },
      })
    );
  });
}
