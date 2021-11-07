import Vue from "vue";
import VueRouter, { NavigationGuardNext, Route, RouteConfig } from "vue-router";
import Home from "@/views/ArtifactTreeView.vue";
import TraceLinks from "@/views/ApproveLinksView.vue";
import { Routes } from "./routes";
import ErrorPage from "@/views/ErrorPageView.vue";
import { appModule, projectModule } from "@/store";

export { Routes };

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: Routes.HOME,
    name: "Home",
    component: Home,
  },
  {
    path: Routes.TRACE_LINK,
    name: "Trace Links",
    component: TraceLinks,
  },
  {
    path: Routes.ERROR,
    name: "Error Page",
    component: ErrorPage,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

const routesWithRequiredProject: string[] = [Routes.TRACE_LINK];

router.beforeEach((to: Route, from: Route, next: NavigationGuardNext) => {
  const isProjectDefined: boolean = projectModule.getProject.projectId !== "";
  if (routesWithRequiredProject.includes(to.path) && !isProjectDefined) {
    appModule.onWarning(
      "Project must be selected before approving trace links."
    );
    next("/");
  } else {
    next();
  }
});

export default router;
