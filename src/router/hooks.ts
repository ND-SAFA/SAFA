import { Routes } from "@/router/routes";
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
  if (router.currentRoute.path === route) {
    return;
  } else {
    await router.push({ path: route, query });
  }
}
