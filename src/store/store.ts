import Vue from "vue";
import Vuex from "vuex";
import { getModule } from "vuex-module-decorators";
import { vuexLocal } from "@/plugins/vuex-persist";

import {
  AppModule,
  ArtifactSelectionModule,
  DeltaModule,
  ErrorModule,
  ProjectModule,
  SessionModule,
  SnackbarModule,
  SubtreeModule,
  ViewportModule,
  LinkDirectionsModule,
  CommitModule,
} from "./modules";

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
    linkDirections: LinkDirectionsModule,
    artifactSelection: ArtifactSelectionModule,
    viewport: ViewportModule,
    commit: CommitModule,
    subtree: SubtreeModule,
    snackbar: SnackbarModule,
  },
  plugins: [vuexLocal.plugin],
});

export const appModule = getModule(AppModule, store);
export const logModule = getModule(SnackbarModule, store);
export const sessionModule = getModule(SessionModule, store);
export const errorModule = getModule(ErrorModule, store);
export const projectModule = getModule(ProjectModule, store);
export const artifactSelectionModule = getModule(
  ArtifactSelectionModule,
  store
);
export const deltaModule = getModule(DeltaModule, store);
export const viewportModule = getModule(ViewportModule, store);
export const commitModule = getModule(CommitModule, store);
export const subtreeModule = getModule(SubtreeModule, store);
export const linkDirectionsModule = getModule(LinkDirectionsModule, store);

export default store;
