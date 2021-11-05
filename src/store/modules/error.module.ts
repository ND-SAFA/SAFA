import type { ProjectWarnings, ProjectErrors } from "@/types";
import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

@Module({ namespaced: true, name: "error" })
/**
 * This module defines the state of errors encountered within the loaded project.
 */
export default class ErrorModule extends VuexModule {
  /**
   * A collection of warnings keyed by the associated artifact.
   */
  private artifactWarnings: ProjectWarnings = {};
  /**
   * A collection of errors encountered within different segments of the project files.
   */
  private projectErrors: ProjectErrors = {
    tim: [],
    artifacts: [],
    traces: [],
  };

  @Action
  /**
   * Sets the current collection of artifact warnings.
   *
   * @param warnings - A new collection of project warnings.
   */
  setArtifactWarnings(warnings: ProjectWarnings): void {
    this.SET_ARTIFACT_WARNINGS(warnings);
  }

  @Mutation
  /**
   * Sets the current collection of artifact warnings.
   *
   * @param warnings - A new collection of project warnings.
   */
  SET_ARTIFACT_WARNINGS(warnings: ProjectWarnings): void {
    this.artifactWarnings = warnings;
  }

  /**
   * @return The current artifact warnings.
   */
  get getArtifactWarnings(): ProjectWarnings {
    return this.artifactWarnings;
  }

  /**
   * @return The current project errors.
   */
  get getProjectErrors(): ProjectErrors {
    return this.projectErrors;
  }
}
