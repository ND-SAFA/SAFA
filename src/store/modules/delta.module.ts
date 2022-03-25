import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type {
  Artifact,
  EntityModification,
  ProjectDelta,
  ProjectVersion,
  TraceLink,
} from "@/types";
import { ArtifactDeltaState, PanelType } from "@/types";
import { createProjectDelta } from "@/util";
import { disableDrawMode } from "@/cytoscape";
import {
  appModule,
  projectModule,
  subtreeModule,
  viewportModule,
} from "@/store";

@Module({ namespaced: true, name: "delta" })
/**
 * This module defines state variables for tracking artifact deltas.
 */
export default class ErrorModule extends VuexModule {
  /**
   * Whether the artifact delta view is currently enabled.
   */
  private isDeltaViewEnabled = false;
  /**
   * The version that artifact deltas have been made to.
   */
  private afterVersion?: ProjectVersion;
  /**
   * A collection of all added artifacts.
   */
  private projectDelta = createProjectDelta();

  @Action
  /**
   * Sets whether the delta view is enabled.
   *
   * @param isDeltaViewEnabled - Whether to enable this view.
   */
  setIsDeltaViewEnabled(isDeltaViewEnabled: boolean): void {
    this.SET_DELTA_IN_VIEW(isDeltaViewEnabled);

    if (isDeltaViewEnabled) {
      disableDrawMode();
    }
  }

  @Action
  /**
   * Sets the current artifact deltas.
   *
   * @param payload - All artifact deltas.
   */
  async setDeltaPayload(payload: ProjectDelta): Promise<void> {
    await this.removeDeltaAdditions();
    this.SET_DELTA_PAYLOAD(payload);
    await projectModule.addOrUpdateArtifacts([
      ...Object.values(payload.artifacts.added),
      ...Object.values(payload.artifacts.removed),
    ]);
    await projectModule.addOrUpdateTraceLinks([
      ...Object.values(payload.traces.added),
      ...Object.values(payload.traces.removed),
    ]);
    await subtreeModule.restoreHiddenNodesAfter(
      viewportModule.setArtifactTreeLayout
    );
  }

  @Action
  /**
   * Sets the version that deltas are made to.
   *
   * @param version - The new version.
   */
  setAfterVersion(version?: ProjectVersion): void {
    this.SET_AFTER_VERSION(version);
  }

  @Action
  /**
   * Clears the current collections of artifact deltas.
   */
  clearDelta(): void {
    this.SET_DELTA_PAYLOAD(createProjectDelta());
    this.SET_DELTA_IN_VIEW(false);
    this.setIsDeltaViewEnabled(false);
    appModule.closePanel(PanelType.right);
  }

  @Action
  /**
   * Removes delta artifacts and traces from the current project.
   */
  async removeDeltaAdditions(): Promise<void> {
    await projectModule.deleteArtifacts(Object.values(this.addedArtifacts));
    await projectModule.deleteTraceLinks(Object.values(this.addedTraces));
  }

  @Mutation
  /**
   * Sets whether the delta view is enabled.
   *
   * @param deltaInView - Whether to enable this view.
   */
  SET_DELTA_IN_VIEW(deltaInView: boolean): void {
    this.isDeltaViewEnabled = deltaInView;
  }

  @Mutation
  /**
   * Sets the current artifact deltas.
   *
   * @param projectDelta - The collections of artifact and trace deltas.
   */
  SET_DELTA_PAYLOAD(projectDelta: ProjectDelta): void {
    this.projectDelta = projectDelta;
  }

  @Mutation
  /**
   * Sets the current version to apply deltas to.
   *
   * @param afterVersion - The new version.
   */
  SET_AFTER_VERSION(afterVersion?: ProjectVersion): void {
    this.afterVersion = afterVersion;
  }

  /**
   * @return A mapping of artifact IDs and the artifacts added.
   */
  get addedArtifacts(): Record<string, Artifact> {
    return this.projectDelta.artifacts.added;
  }

  /**
   * @return A mapping of artifact IDs and the artifacts removed.
   */
  get removedArtifacts(): Record<string, Artifact> {
    return this.projectDelta.artifacts.removed;
  }

  /**
   * @return A collection of modified deltas.
   */
  get modifiedArtifacts(): Record<string, EntityModification<Artifact>> {
    return this.projectDelta.artifacts.modified;
  }

  /**
   * @return A mapping of trace IDs and the traces added.
   */
  get addedTraces(): Record<string, TraceLink> {
    return this.projectDelta.traces.added;
  }

  /**
   * @return The current version that deltas are made to.
   */
  get deltaVersion(): ProjectVersion | undefined {
    return this.afterVersion;
  }

  /**
   * @return Whether the delta view is currently enabled.
   */
  get inDeltaView(): boolean {
    return this.isDeltaViewEnabled;
  }

  /**
   * @return All delta states that associated with the artifacts given artifact names.
   */
  get getDeltaStatesByArtifactNames(): (
    names: string[]
  ) => ArtifactDeltaState[] {
    return (names) => {
      const deltaStates = new Set<ArtifactDeltaState>();

      for (const name of names) {
        if (name in this.projectDelta.artifacts.added) {
          deltaStates.add(ArtifactDeltaState.ADDED);
        } else if (name in this.projectDelta.artifacts.modified) {
          deltaStates.add(ArtifactDeltaState.MODIFIED);
        } else if (name in this.projectDelta.artifacts.removed) {
          deltaStates.add(ArtifactDeltaState.REMOVED);
        }
      }

      return Array.from(deltaStates);
    };
  }

  /**
   * @return The delta state of the given trace link id.
   */
  get getTraceDeltaType(): (id: string) => ArtifactDeltaState | undefined {
    return (id) => {
      if (!this.inDeltaView) {
        return undefined;
      } else if (id in this.projectDelta.traces.added) {
        return ArtifactDeltaState.ADDED;
      } else if (id in this.projectDelta.traces.modified) {
        return ArtifactDeltaState.MODIFIED;
      } else if (id in this.projectDelta.traces.removed) {
        return ArtifactDeltaState.REMOVED;
      }
    };
  }

  /**
   * @return The delta state of the given artifacts id.
   */
  get getArtifactDeltaType(): (id: string) => ArtifactDeltaState | undefined {
    return (id) => {
      if (!this.inDeltaView) {
        return undefined;
      } else if (id in this.projectDelta.artifacts.added) {
        return ArtifactDeltaState.ADDED;
      } else if (id in this.projectDelta.artifacts.modified) {
        return ArtifactDeltaState.MODIFIED;
      } else if (id in this.projectDelta.artifacts.removed) {
        return ArtifactDeltaState.REMOVED;
      } else {
        return ArtifactDeltaState.NO_CHANGE;
      }
    };
  }
}
