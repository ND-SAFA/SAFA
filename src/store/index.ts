import Vue from "vue";
import Vuex from "vuex";
import { getModule } from "vuex-module-decorators";
import {
  AppModule,
  ArtifactSelectionModule,
  DeltaModule,
  ErrorModule,
  ProjectModule,
  SessionModule,
  ViewportModule,
} from "./modules";

import "./routerStore";

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

export default store;
