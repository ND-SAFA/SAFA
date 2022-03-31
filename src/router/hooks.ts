import { QueryParams, Routes } from "@/router/routes";
import router from "@/router/router";

/**
 * Navigates app to given route, if app is already on the route then
 * does nothing. This wrapper stops DuplicateNavigation exceptions.
 *
 * @param route - The route to navigate to.
 * @param query - Any query params to include.
 */
export async function navigateTo(
  route: Routes | string,
  query?: Record<string, string>
): Promise<void> {
  if (router.currentRoute.path === route && !query) {
    return;
  } else {
    await router.push({ path: route, query });
  }
}

/**
 * Return the app's query parameters.
 *
 * @param key - The query param key.
 */
export function getParam(key: QueryParams): string | (string | null)[] {
  return router.currentRoute.query[key];
}

/**
 * Changes the app's query parameters.
 *
 * @param key - The query param key.
 * @param value - The query param value.
 */
export async function updateParam(key: string, value: string): Promise<void> {
  if (router.currentRoute.query[key] !== value) {
    return navigateTo(router.currentRoute.path, { [key]: value });
  }
}
