import { ArtifactWarning, ProjectWarnings, ProjectErrors } from "@/types";
import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

@Module({ namespaced: true, name: "error" })
export default class ErrorModule extends VuexModule {
  artifactWarnings: Record<string, ArtifactWarning[]> = {};
  projectErrors: ProjectErrors = {
    tim: [],
    artifacts: [],
    traces: [],
  };

  @Action
  setArtifactWarnings(warnings: ProjectWarnings): void {
    this.SET_ARTIFACT_WARNINGS(warnings);
  }

  @Mutation
  SET_ARTIFACT_WARNINGS(warnings: ProjectWarnings): void {
    this.artifactWarnings = warnings;
  }

  get getArtifactWarnings(): ProjectWarnings {
    return this.artifactWarnings;
  }
  get getProjectErrors(): ProjectErrors {
    return this.projectErrors;
  }
}
