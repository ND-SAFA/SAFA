import Vue from "vue";
import VueRouter, { NavigationGuardNext, Route, RouteConfig } from "vue-router";
import Home from "@/views/ArtifactTreeView.vue";
import TraceLinks from "@/views/ApproveLinksView.vue";
import { ERROR_ROUTE_NAME, TRACE_LINK_ROUTE_NAME } from "@/router/routes";
import ErrorPage from "@/views/ErrorPageView.vue";
import store, { appModule, projectModule } from "@/store";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: TRACE_LINK_ROUTE_NAME,
    name: "Trace Links",
    component: TraceLinks,
  },
  {
    path: ERROR_ROUTE_NAME,
    name: "Error Page",
    component: ErrorPage,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

const routesWithRequiredProject = [TRACE_LINK_ROUTE_NAME];

router.beforeEach((to: Route, from: Route, next: NavigationGuardNext) => {
  const isProjectDefined: boolean = projectModule.getProject.projectId !== "";
  if (routesWithRequiredProject.includes(to.path) && !isProjectDefined) {
    appModule.onWarning(
      "Project must be selected before approving trace links"
    );
    next("/");
  } else {
    next();
  }
});

export default router;
