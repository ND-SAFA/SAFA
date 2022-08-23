import { defineStore } from "pinia";
import { createProject } from "@/util";
import { pinia } from "@/plugins";
import {
  ArtifactModel,
  ArtifactTypeModel,
  ProjectModel,
  TraceLinkModel,
  VersionModel,
} from "@/types";
import { warningStore } from "@/hooks";
import layoutStore from "../graph/useLayout";
import logStore from "../core/useLog";
import documentStore from "./useDocuments";
import subtreeStore from "./useSubtree";
import typeOptionsStore from "./useTypeOptions";
import artifactStore from "./useArtifacts";
import traceStore from "./useTraces";

/**
 * Manages the selected project.
 */
export const useProject = defineStore("project", {
  state: () => ({
    /**
     * The currently loaded project.
     */
    project: createProject(),
  }),
  getters: {
    /**
     * @return The current project id.
     */
    projectId(): string {
      return this.project.projectId;
    },
    /**
     * @return The current version.
     */
    version(): VersionModel | undefined {
      return this.project.projectVersion;
    },
    /**
     * @return The current version id.
     */
    versionId(): string {
      return this.version?.versionId || "";
    },
    /**
     * @returns Whether the project is defined.
     */
    isProjectDefined(): boolean {
      return this.projectId !== "";
    },
    /**
     * @returns Whether the version is defined.
     */
    isVersionDefined(): boolean {
      return this.versionId !== "";
    },
    /**
     * @return Returns the version ID, and logs an error if there isn't one.
     */
    versionIdWithLog(): string {
      if (!this.versionId) {
        logStore.onWarning("Please select a project version.");
      }

      return this.versionId;
    },
  },
  actions: {
    /**
     * Updates the current project.
     *
     * @param project - The new project fields.
     */
    updateProject(project: Partial<ProjectModel>): void {
      this.project = {
        ...this.project,
        ...project,
      };
    },
    /**
     * Initializes the current project.
     */
    initializeProject(project: ProjectModel): void {
      this.project = project;

      layoutStore.artifactPositions = project.layout;
      typeOptionsStore.initializeTypeIcons(project.artifactTypes);
      documentStore.initializeProject(project);
      subtreeStore.initializeProject(project);
      warningStore.artifactWarnings = project.warnings;
    },
    /**
     * Updates the current artifacts in the project, preserving any that already existed.
     *
     * @param newArtifacts - The new artifacts to add.
     */
    addOrUpdateArtifacts(newArtifacts: ArtifactModel[]): void {
      const newIds = newArtifacts.map(({ id }) => id);
      const updatedArtifacts = [
        ...this.project.artifacts.filter(({ id }) => !newIds.includes(id)),
        ...newArtifacts,
      ];

      this.updateProject({
        artifacts: updatedArtifacts,
      });

      artifactStore.initializeArtifacts({
        artifacts: updatedArtifacts,
        currentArtifactIds: documentStore.currentDocument.artifactIds,
      });
      typeOptionsStore.addArtifactTypes(newArtifacts);
      subtreeStore.updateSubtreeMap();
    },
    /**
     * Deletes the given artifacts.
     *
     * @param artifacts - The artifacts to delete.
     */
    deleteArtifacts(artifacts: ArtifactModel[]): void {
      if (artifacts.length === 0) return;

      const deletedNames = artifacts.map(({ name }) => name);

      this.updateProject({
        artifacts: this.project.artifacts.filter(
          ({ name }) => !deletedNames.includes(name)
        ),
      });

      artifactStore.deleteArtifacts(artifacts);
      subtreeStore.updateSubtreeMap();
    },
    /**
     * Updates the current trace links in the project, preserving any that already existed.
     *
     * @param newTraces - The trace links to add.
     */
    addOrUpdateTraceLinks(newTraces: TraceLinkModel[]): void {
      const newIds = newTraces.map(({ traceLinkId }) => traceLinkId);
      const updatedTraces = [
        ...this.project.traces.filter(
          ({ traceLinkId }) => !newIds.includes(traceLinkId)
        ),
        ...newTraces,
      ];

      this.updateProject({ traces: updatedTraces });

      traceStore.initializeTraces({
        traces: updatedTraces,
        currentArtifactIds: documentStore.currentDocument.artifactIds,
      });
      subtreeStore.updateSubtreeMap();
      layoutStore.applyAutomove();
    },
    /**
     * Deletes the given trace link.
     *
     * @param traceLinks - The trace link to remove.
     */
    async deleteTraceLinks(traceLinks: TraceLinkModel[]): Promise<void> {
      if (traceLinks.length === 0) return;

      const deletedIds = traceLinks.map(({ traceLinkId }) => traceLinkId);

      this.updateProject({
        traces: this.project.traces.filter(
          ({ traceLinkId }) => !deletedIds.includes(traceLinkId)
        ),
      });

      traceStore.deleteTraceLinks(traceLinks);
      subtreeStore.updateSubtreeMap();
      layoutStore.applyAutomove();
    },
    /**
     * Adds a new artifact type.
     *
     * @param artifactType - The artifact type to add.
     */
    addOrUpdateArtifactType(artifactType: ArtifactTypeModel): void {
      const unaffectedTypes = this.project.artifactTypes.filter(
        (a) => a.typeId !== artifactType.typeId
      );
      const allArtifactTypes = [...unaffectedTypes, artifactType];

      this.updateProject({
        artifactTypes: allArtifactTypes,
      });

      typeOptionsStore.allArtifactTypes = allArtifactTypes;
    },
    /**
     * Runs the callback only if the project is defined. Otherwise logs a warning.
     *
     * @param cb - The callback to run.
     */
    ifProjectDefined(cb: () => void): void {
      if (this.isProjectDefined) {
        cb();
      } else {
        logStore.onWarning("Please select a project.");
      }
    },
  },
});

export default useProject(pinia);
