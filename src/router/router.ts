import { createRouter, createWebHistory } from "vue-router";
import { routerAfterChecks, routerBeforeChecks } from "@/router/checks";
import { routes } from "./routes";

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
router.beforeEach(async (to, from) => {
  for (const check of Object.values(routerBeforeChecks)) {
    const redirect = await check(to, from);

    if (!redirect) continue;

    return redirect;
  }
});

router.afterEach(async (to, from) => {
  for (const check of Object.values(routerAfterChecks)) {
    const redirect = await check(to, from);

    if (!redirect) continue;

    return redirect;
  }
});
