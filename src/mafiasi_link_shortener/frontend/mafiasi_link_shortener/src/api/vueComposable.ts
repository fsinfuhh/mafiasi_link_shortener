import type { Ref } from "vue";
import { LinksApi } from "@/api/apis";
import { computed } from "vue";
import { Configuration } from "@/api/runtime";
import { useAuthenticatedUser } from "@/auth";

export function useLinksApi(): Ref<LinksApi | null> {
  const user = useAuthenticatedUser()!;

  return computed(() => {
    if (user.value == null) {
      return null;
    }

    return new LinksApi(
      new Configuration({
        basePath: window.config.VITE_API_BASE as string,
        headers: {
          Authorization: `Bearer ${user.value!.access_token}`,
        },
      })
    );
  });
}
