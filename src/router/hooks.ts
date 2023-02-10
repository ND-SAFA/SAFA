import { useRoute, useRouter } from "vue-router";
import { URLParameter } from "@/types";
import { QueryParams, Routes } from "@/router/routes";
import { router } from "@/router/router";

/**
 * Navigates app to given route, if app is already on the route then
 * does nothing. This wrapper stops DuplicateNavigation exceptions.
 *
 * @param route - The route to navigate to.
 * @param query - Any query params to include.
 */
export async function navigateTo(
  route: Routes | string,
  query: Record<string, null | string | (string | null)[]> = {}
): Promise<void> {
  if (
    router.currentRoute.value.path === route &&
    Object.keys(query).length === 0
  ) {
    return;
  } else {
    await router.push({ path: route, query });
  }
}

/**
 * Navigates to the previous page.
 */
export function navigateBack(): void {
  router.back();
}

/**
 * Return the app's query parameters.
 */
export function getParams(): Record<string, null | string | (string | null)[]> {
  return router.currentRoute.value.query;
}

/**
 * Return one of the app's query parameters.
 *
 * @param key - The query param key.
 * @return The query parameter value.
 */
export function getParam(key: QueryParams): URLParameter {
  return router.currentRoute.value.query[key];
}

/**
 * Changes the app's query parameters.
 *
 * @param key - The query param key.
 * @param value - The query param value.
 */
export async function updateParam(key: string, value: string): Promise<void> {
  const currentRoute = router.currentRoute.value;

  if (currentRoute.query[key] === value) return;

  return navigateTo(currentRoute.path, { [key]: value });
}

/**
 * Removes all query parameters.
 */
export async function removeParams(): Promise<void> {
  const currentRoute = router.currentRoute.value;

  if (Object.values(currentRoute.query).length === 0) return;

  return navigateTo(currentRoute.path, {});
}
