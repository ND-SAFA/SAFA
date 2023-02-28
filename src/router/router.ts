import { createRouter, createWebHistory } from "vue-router";
import { routerChecks } from "@/router/checks";
import { routes } from "./routes";

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

/**
 * Iterates through each router check and exits after the first check
 * uses the next function.
 */
router.beforeResolve(async (to, from) => {
  for (const check of Object.values(routerChecks)) {
    const redirect = await check(to, from);

    if (!redirect) continue;

    return redirect;
  }
});
