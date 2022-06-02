import type { ProjectWarnings, ArtifactWarning } from "@/types";
import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

@Module({ namespaced: true, name: "warning" })
/**
 * This module defines the state of warnings generated for
 * artifacts and traces in this version.
 */
export default class WarningModule extends VuexModule {
  /**
   * A collection of warnings keyed by the associated artifact.
   */
  private artifactWarnings: ProjectWarnings = {};

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
   * @return Warnings associated with artifacts of given names.
   */
  get getWarningsByArtifactNames(): (names: string[]) => ArtifactWarning[] {
    return (names) => {
      return names
        .map((name) => this.artifactWarnings[name] || [])
        .reduce((acc, cur) => [...acc, ...cur], []);
    };
  }
}
