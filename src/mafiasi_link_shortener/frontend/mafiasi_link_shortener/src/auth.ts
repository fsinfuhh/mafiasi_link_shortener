import { User, UserManager } from "oidc-client-ts";
import { inject } from "vue";
import type { Ref } from "vue";
import { useAuthStore } from "@/stores";

export const USER_MANGER_SYMBOL = Symbol("user-manager");

/**
 * Create a new `UserManager` instance based on runtime settings defined through the environment.
 */
export function createUserManager(): UserManager {
  return new UserManager({
    authority: window.config.VITE_OPENID_ISSUER as string,
    client_id: window.config.VITE_OPENID_CLIENT_ID as string,
    scope: window.config.VITE_OPENID_SCOPE as string,
    redirect_uri: window.location.toString(),
  });
}

/**
 * Remove url parameters from the current URL that relate to the OAuth authentication
 */
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
