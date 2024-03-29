import type { Ref } from "vue";
import { LinksApi, LoggedInApi } from "@/api/apis";
import { computed } from "vue";
import { Configuration } from "@/api/runtime";
import { useAuthStore } from "@/stores";

export function useLinksApi(): Ref<LinksApi | null> {
  const authStore = useAuthStore();

  return computed(() => {
    if (!authStore.isAuthenticated) {
      return null;
    }

    const csrf_token = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken"))
      ?.split("=")[1];
    let headers = {};
    if (csrf_token) {
      headers = {
        "X-CSRFToken": csrf_token,
      };
    }

    return new LinksApi(
      new Configuration({
        basePath: window.config.VITE_API_BASE as string,
        credentials: "include",
        headers: headers,
      })
    );
  });
}

export function useLoggedInApi(): LoggedInApi {
  return new LoggedInApi(
    new Configuration({
      basePath: window.config.VITE_API_BASE as string,
      credentials: "include",
    })
  );
}
