import Vue from "vue";
import Vuex from "vuex";
import { getModule } from "vuex-module-decorators";
import { NavigationGuardNext, Route } from "vue-router";
import {
  AppModule,
  ArtifactSelectionModule,
  DeltaModule,
  ErrorModule,
  ProjectModule,
  SessionModule,
  ViewportModule,
} from "./modules";
import {
  Routes,
  routesPublic,
  routesWithRequiredProject,
} from "@/router/routes";
import router from "@/router";
import { sessionIsLoaded } from "@/store/modules/session.module";

Vue.use(Vuex);
Vue.config.devtools = true;

const store = new Vuex.Store({
  mutations: {},
  actions: {},
  modules: {
    session: SessionModule,
    app: AppModule,
    project: ProjectModule,
    delta: DeltaModule,
    error: ErrorModule,
    artifactSelection: ArtifactSelectionModule,
    viewport: ViewportModule,
  },
});

export const sessionModule = getModule(SessionModule, store);
export const errorModule = getModule(ErrorModule, store);
export const projectModule = getModule(ProjectModule, store);
export const appModule = getModule(AppModule, store);
export const artifactSelectionModule = getModule(
  ArtifactSelectionModule,
  store
);
export const deltaModule = getModule(DeltaModule, store);
export const viewportModule = getModule(ViewportModule, store);

router.beforeResolve((to: Route, from: Route, next: NavigationGuardNext) => {
  if (!routesPublic.includes(to.path) && !sessionIsLoaded) {
    next(Routes.LOGIN_ACCOUNT);
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

export default store;
