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
  TypeOptionsModule,
  CommitModule,
  DocumentModule,
  ArtifactModule,
  TraceModule,
  JobModule,
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
    document: DocumentModule,
    artifact: ArtifactModule,
    trace: TraceModule,
    delta: DeltaModule,
    error: ErrorModule,
    typeOptions: TypeOptionsModule,
    artifactSelection: ArtifactSelectionModule,
    viewport: ViewportModule,
    commit: CommitModule,
    subtree: SubtreeModule,
    snackbar: SnackbarModule,
    job: JobModule,
  },
  plugins: [vuexLocal.plugin],
});

export const appModule = getModule(AppModule, store);
export const logModule = getModule(SnackbarModule, store);
export const sessionModule = getModule(SessionModule, store);
export const errorModule = getModule(ErrorModule, store);
export const projectModule = getModule(ProjectModule, store);
export const documentModule = getModule(DocumentModule, store);
export const artifactModule = getModule(ArtifactModule, store);
export const traceModule = getModule(TraceModule, store);
export const artifactSelectionModule = getModule(
  ArtifactSelectionModule,
  store
);
export const deltaModule = getModule(DeltaModule, store);
export const viewportModule = getModule(ViewportModule, store);
export const commitModule = getModule(CommitModule, store);
export const subtreeModule = getModule(SubtreeModule, store);
export const typeOptionsModule = getModule(TypeOptionsModule, store);
export const jobModule = getModule(JobModule, store);

export default store;
