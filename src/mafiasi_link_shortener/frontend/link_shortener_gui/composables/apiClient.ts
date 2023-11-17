import {Configuration, LinksApi} from "~/utils/apiClient";

async function useApiConfig(): Promise<Configuration> {
    const config = useRuntimeConfig();
    const userManager = useUserManager();

    return new Configuration({
        basePath: config.public.apiBase,
        headers: {
            "Authorization": `Bearer ${(await userManager.getUser())!.access_token}`,
        }
    })
}

export async function useLinksApi(): Promise<LinksApi> {
    return new LinksApi(await useApiConfig())
}
