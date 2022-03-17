import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

import type {
  Artifact,
  ArtifactQueryFunction,
  DocumentArtifacts,
} from "@/types";
import { getSingleQueryResult } from "@/util";
import { artifactSelectionModule, documentModule } from "@/store";

@Module({ namespaced: true, name: "artifact" })
/**
 * This module defines the state of the currently visible artifacts.
 */
export default class ArtifactModule extends VuexModule {
  /**
   * All artifacts in the project.
   */
  private projectArtifacts: Artifact[] = [];
  /**
   * The currently visible artifacts.
   */
  private currentArtifacts: Artifact[] = [];

  @Action
  /**
   * Initializes the artifacts visible in the current document.
   */
  initializeArtifacts(documentArtifacts: DocumentArtifacts): void {
    const { artifacts = this.projectArtifacts, currentArtifactIds } =
      documentArtifacts;

    this.SET_PROJECT_ARTIFACTS(artifacts);
    this.SET_CURRENT_ARTIFACTS(
      currentArtifactIds
        ? artifacts.filter(({ id }) => currentArtifactIds.includes(id))
        : artifacts
    );
  }

  @Action
  /**
   * Updates the current artifacts in the project, preserving any that already existed.
   *
   * @param artifacts - The artifacts to set.
   */
  async addOrUpdateArtifacts(updatedArtifacts: Artifact[]): Promise<void> {
    const visibleIds = documentModule.document.artifactIds;
    const visibleArtifacts = updatedArtifacts.filter(({ id }) =>
      visibleIds.includes(id)
    );

    this.SET_PROJECT_ARTIFACTS(updatedArtifacts);
    this.SET_CURRENT_ARTIFACTS(visibleArtifacts);

    const selectedArtifact = artifactSelectionModule.getSelectedArtifact;

    if (selectedArtifact !== undefined) {
      const query = updatedArtifacts.filter(
        ({ name }) => name === selectedArtifact.name
      );
      if (query.length > 0) {
        artifactSelectionModule.selectArtifact(query[0].id);
      }
    }
  }

  @Action
  /**
   * Deletes the artifact with the given name.
   */
  async deleteArtifacts(artifacts: Artifact[]): Promise<void> {
    const deletedNames = artifacts.map(({ name }) => name);
    const removeArtifact = (currentArtifacts: Artifact[]) =>
      currentArtifacts.filter(({ name }) => !deletedNames.includes(name));

    this.SET_PROJECT_ARTIFACTS(removeArtifact(this.projectArtifacts));
    this.SET_CURRENT_ARTIFACTS(removeArtifact(this.currentArtifacts));
  }

  @Mutation
  /**
   * Sets the project artifacts.
   */
  SET_PROJECT_ARTIFACTS(artifacts: Artifact[]): void {
    this.projectArtifacts = artifacts;
  }

  @Mutation
  /**
   * Sets the current artifacts.
   */
  SET_CURRENT_ARTIFACTS(artifacts: Artifact[]): void {
    this.currentArtifacts = artifacts;
  }

  /**
   * @return All artifacts in the project.
   */
  get allArtifacts(): Artifact[] {
    return this.projectArtifacts;
  }

  /**
   * @return The artifacts for the current document.
   */
  get artifacts(): Artifact[] {
    return this.currentArtifacts;
  }

  /**
   * @return A function for finding an artifact by name.
   * @throws If more or less than 1 artifact is found to match.
   */
  get getArtifactByName(): ArtifactQueryFunction {
    return (artifactName) => {
      const query = this.artifacts.filter((a) => a.name === artifactName);

      return getSingleQueryResult(query, `Find by name: ${artifactName}`);
    };
  }

  /**
   * @return A function for finding an artifact by id.
   * @throws If more or less than 1 artifact is found to match.
   */
  get getArtifactById(): ArtifactQueryFunction {
    return (targetArtifactId) => {
      const query = this.artifacts.filter((a) => a.id === targetArtifactId);

      return getSingleQueryResult(query, `Find by id: ${targetArtifactId}`);
    };
  }

  /**
   * @return A collection of artifacts, keyed by their id.
   */
  get getArtifactsById(): Record<string, Artifact> {
    return this.artifacts
      .map((artifact) => ({ [artifact.id]: artifact }))
      .reduce((acc, cur) => ({ ...acc, ...cur }), {});
  }
}
