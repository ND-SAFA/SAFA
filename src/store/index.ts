import Vue from "vue";
import Vuex from "vuex";
import AppModule from "@/store/modules/app.module";
import ProjectModule from "@/store/modules/project.module";
import DeltaModule from "@/store/modules/delta.module";
import ArtifactSelectionModule from "@/store/modules/graph.module";
import ErrorModule from "@/store/modules/error.module";
import { getModule } from "vuex-module-decorators";
import ViewportModule from "@/store/modules/viewport.module";

Vue.use(Vuex);
Vue.config.devtools = true;

const store = new Vuex.Store({
  mutations: {},
  actions: {},
  modules: {
    app: AppModule,
    project: ProjectModule,
    delta: DeltaModule,
    error: ErrorModule,
    artifactSelection: ArtifactSelectionModule,
    viewport: ViewportModule,
  },
});

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
