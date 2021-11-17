import router, { Routes } from "@/router";
import { NavigationGuardNext, Route } from "vue-router";
import { routesPublic, routesWithRequiredProject } from "@/router/routes";
import { sessionIsLoaded } from "@/store/modules/session.module";
import { appModule, projectModule } from "@/store/index";

router.beforeResolve((to: Route, from: Route, next: NavigationGuardNext) => {
  if (!routesPublic.includes(to.path) && !sessionIsLoaded) {
    next({ path: Routes.LOGIN_ACCOUNT, query: { to: to.path } });
    return;
  }

  const isProjectDefined = projectModule.getProject.projectId !== "";

  if (routesWithRequiredProject.includes(to.path) && !isProjectDefined) {
    appModule.onWarning(
      "Project must be selected before approving trace links."
    );
    next(Routes.HOME);
  } else {
    next();
  }
});
