import Vue from "vue";
import VueRouter, { NavigationGuardNext, Route, RouteConfig } from "vue-router";
import { Routes } from "./routes";
import { appModule, projectModule } from "@/store";
import {
  ErrorPageView,
  ApproveLinksView,
  ArtifactTreeView,
  ProjectCreatorView,
} from "@/views";

export { Routes };

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: Routes.HOME,
    name: "Home",
    component: ProjectCreatorView,
  },
  {
    path: Routes.ARTIFACT_TREE,
    name: "Artifact Tree",
    component: ArtifactTreeView,
  },
  {
    path: Routes.TRACE_LINK,
    name: "Trace Links",
    component: ApproveLinksView,
  },
  {
    path: Routes.PROJECT_CREATOR,
    name: "Project Creator",
    component: ProjectCreatorView,
  },
  {
    path: Routes.ERROR,
    name: "Error Page",
    component: ErrorPageView,
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
