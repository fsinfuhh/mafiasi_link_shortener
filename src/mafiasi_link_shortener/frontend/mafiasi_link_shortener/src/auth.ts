import { User, UserManager } from "oidc-client-ts";
import { inject, onMounted, ref } from "vue";
import type { Ref } from "vue";

export const USER_MANGER_SYMBOL = Symbol("user-manager");

export function createUserManager(): UserManager {
  return new UserManager({
    authority: window.config.VITE_OPENID_ISSUER as string,
    client_id: window.config.VITE_OPENID_CLIENT_ID as string,
    scope: window.config.VITE_OPENID_SCOPE as string,
    redirect_uri: window.location.toString(),
  });
}

export function useUserManager(): UserManager | undefined {
  return inject(USER_MANGER_SYMBOL);
}

function removeCallbackInfoFromUrl(): void {
  const url = new URL(window.location.toString());
  url.search = "";
  window.history.replaceState(null, "", url.toString());
}

/**
 * Try to retrieve user information or perform a login if that is not possible.
 *
 * **Caution** This function redirects the user in order to log them in so the user agent may leave the app.
 */
// @ts-ignore
export async function getUserOrLogin(userManager: UserManager): Promise<User | never> {
  try {
    // try to fetch the user from authentication result
    const user = await userManager.signinRedirectCallback();
    removeCallbackInfoFromUrl();
    return user;
  } catch (e: unknown) {
    const error = e as Error;

    if (error.message == "No state in response") {
      // no user is known and no callback state in current url
      await userManager.signinRedirect();
    } else if (error.message == "No matching state found in storage") {
      // there is callback info in the current url, but it is not valid
      removeCallbackInfoFromUrl();
      await userManager.signinRedirect();
    } else {
      throw e;
    }
  }
}

/**
 * Get a reference to the currently authenticated user.
 * If no user is currently authenticated, automatically perform a login.
 *
 * **Caution** This function redirects the user in order to log them in so the user agent may leave the app.
 */
export function useAuthenticatedUser(): Ref<User | null> | never {
  const userManager = useUserManager();
  const value = ref<User | null>(null);

  onMounted(async () => {
    if (userManager == undefined) {
      console.warn("useAuthenticatedUser() was called but userManager could not be injected");
      return;
    }

    value.value = await getUserOrLogin(useUserManager()!);
  });

  return value;
}
