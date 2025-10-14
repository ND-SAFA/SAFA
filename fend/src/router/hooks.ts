import { URLParameter, URLQuery } from "@/types";
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
  query: URLQuery = {}
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
export function getParams(): URLQuery {
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
 * @param preserveQuery - Whether to preserve the current query parameters.
 */
export async function updateParam(
  key: string,
  value: string | undefined,
  preserveQuery?: boolean
): Promise<void> {
  const currentRoute = router.currentRoute.value;
  const query = preserveQuery
    ? { ...currentRoute.query, [key]: value }
    : { [key]: value };

  if (currentRoute.query[key] === value) return;

  return navigateTo(currentRoute.path, query);
}

/**
 * Removes all query parameters.
 */
export async function removeParams(): Promise<void> {
  if (Object.keys(router.currentRoute.value.query).length === 0) return;

  await router.replace({ query: {} });
}
