import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

import type {
  ArtifactModel,
  ArtifactQueryFunction,
  DocumentArtifacts,
} from "@/types";
import { getSingleQueryResult } from "@/util";
import { artifactSelectionModule, documentModule } from "@/store";
import { FlatArtifact } from "@/types";

@Module({ namespaced: true, name: "artifact" })
/**
 * This module defines the state of the currently visible artifacts.
 */
export default class ArtifactModule extends VuexModule {
  /**
   * All artifacts in the project.
   */
  private projectArtifacts: ArtifactModel[] = [];
  /**
   * The currently visible artifacts.
   */
  private currentArtifacts: ArtifactModel[] = [];

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
   * DO NOT CALL THIS OUTSIDE OF THE PROJECT MODULE.
   * Updates the current artifacts in the project, preserving any that already existed.
   *
   * @param artifacts - The artifacts to set.
   */
  async addOrUpdateArtifacts(updatedArtifacts: ArtifactModel[]): Promise<void> {
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
   * DO NOT CALL THIS OUTSIDE OF THE PROJECT MODULE.
   * Deletes the artifact with the given name.
   */
  async deleteArtifacts(artifacts: ArtifactModel[]): Promise<void> {
    const deletedNames = artifacts.map(({ name }) => name);
    const removeArtifact = (currentArtifacts: ArtifactModel[]) =>
      currentArtifacts.filter(({ name }) => !deletedNames.includes(name));
    this.SET_PROJECT_ARTIFACTS(removeArtifact(this.projectArtifacts));
    this.SET_CURRENT_ARTIFACTS(removeArtifact(this.currentArtifacts));
  }

  @Mutation
  /**
   * Sets the project artifacts.
   */
  SET_PROJECT_ARTIFACTS(artifacts: ArtifactModel[]): void {
    this.projectArtifacts = artifacts;
  }

  @Mutation
  /**
   * Sets the current artifacts.
   */
  SET_CURRENT_ARTIFACTS(artifacts: ArtifactModel[]): void {
    this.currentArtifacts = artifacts;
  }

  /**
   * @return All artifacts in the project.
   */
  get allArtifacts(): ArtifactModel[] {
    return this.projectArtifacts;
  }

  /**
   * @return The artifacts for the current document.
   */
  get artifacts(): ArtifactModel[] {
    return this.currentArtifacts;
  }

  /**
   * @return The flattened artifacts for the current document.
   */
  get flatArtifacts(): FlatArtifact[] {
    return this.currentArtifacts.map(
      (artifact) =>
        ({
          ...artifact,
          ...artifact.customFields,
        } as FlatArtifact)
    );
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
      const query = this.allArtifacts.filter((a) => a.id === targetArtifactId);

      return getSingleQueryResult(query, `Find by id: ${targetArtifactId}`);
    };
  }

  /**
   * @return A collection of artifacts, keyed by their id.
   */
  get getArtifactsById(): Record<string, ArtifactModel> {
    return this.artifacts
      .map((artifact) => ({ [artifact.id]: artifact }))
      .reduce((acc, cur) => ({ ...acc, ...cur }), {});
  }

  /**
   * @return A collection of artifact lists, keyed by their type.
   */
  get getArtifactsByType(): Record<string, ArtifactModel[]> {
    const artifactsByType: Record<string, ArtifactModel[]> = {};

    this.artifacts.forEach((artifact) => {
      if (!artifactsByType[artifact.type]) {
        artifactsByType[artifact.type] = [];
      }

      artifactsByType[artifact.type].push(artifact);
    });

    return artifactsByType;
  }
}
