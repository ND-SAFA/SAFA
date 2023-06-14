import { defineStore } from "pinia";

import {
  ApprovalType,
  ArtifactDeltaState,
  ArtifactSchema,
  EntityModification,
  GraphMode,
  ProjectDelta,
  TraceLinkSchema,
  VersionSchema,
} from "@/types";
import { createProjectDelta } from "@/util";
import { disableDrawMode } from "@/cytoscape";
import { pinia } from "@/plugins";
import layoutStore from "../graph/useLayout";
import appStore from "../core/useApp";
import subtreeStore from "./useSubtree";
import artifactStore from "./useArtifacts";
import traceStore from "./useTraces";

/**
 * This module tracks the delta state of a project.
 */
export const useDelta = defineStore("delta", {
  state: () => ({
    /**
     * Whether the artifact delta view is currently enabled.
     */
    inDeltaView: false,
    /**
     * The version that artifact deltas have been made to.
     */
    afterVersion: undefined as VersionSchema | undefined,
    /**
     * A collection of all added artifacts.
     */
    projectDelta: createProjectDelta(),
  }),
  getters: {
    /**
     * @return A collection of all added artifacts.
     */
    addedArtifacts(): Record<string, ArtifactSchema> {
      return this.projectDelta.artifacts.added;
    },
    /**
     * @return A collection of all removed artifacts.
     */
    removedArtifacts(): Record<string, ArtifactSchema> {
      return this.projectDelta.artifacts.removed;
    },
    /**
     * @return A collection of all modified artifacts.
     */
    modifiedArtifacts(): Record<string, EntityModification<ArtifactSchema>> {
      return this.projectDelta.artifacts.modified;
    },
    /**
     * @return A collection of all added traces.
     */
    addedTraces(): Record<string, TraceLinkSchema> {
      return this.projectDelta.traces.added;
    },
    /**
     * @return A collection of all removed traces.
     */
    removedTraces(): Record<string, TraceLinkSchema> {
      return this.projectDelta.traces.removed;
    },
  },
  actions: {
    /**
     * Sets whether the delta view is enabled.
     *
     * @param isDeltaViewEnabled - Whether to enable this view.
     */
    setIsDeltaViewEnabled(isDeltaViewEnabled: boolean): void {
      if (this.inDeltaView && !isDeltaViewEnabled) {
        layoutStore.mode = GraphMode.tim;
        this.afterVersion = undefined;
      } else {
        appStore.closeSidePanels();
      }

      this.inDeltaView = isDeltaViewEnabled;

      disableDrawMode();
    },
    /**
     * Clears the current delta and resets the graph state.
     */
    clear(): void {
      this.setIsDeltaViewEnabled(false);
      this.$reset();
    },
    /**
     * Sets the current artifact deltas.
     *
     * @param payload - All artifact deltas.
     */
    async setDeltaPayload(payload: ProjectDelta): Promise<void> {
      this.projectDelta = payload;

      const artifacts = [
        ...Object.values(payload.artifacts.added),
        ...Object.values(payload.artifacts.modified).map(({ after }) => after),
        ...Object.values(payload.artifacts.removed),
      ];
      const traces = [
        ...Object.values(payload.traces.added),
        ...Object.values(payload.traces.modified).map(({ after }) => after),
      ];

      artifactStore.addOrUpdateArtifacts(artifacts);
      traceStore.addOrUpdateTraceLinks(traces);

      artifactStore.initializeArtifacts({
        currentArtifactIds: artifacts
          .map(({ id }) => [
            id,
            ...(subtreeStore.subtreeMap[id]?.neighbors || []),
          ])
          .reduce((acc, cur) => [...acc, ...cur], []),
      });
      await subtreeStore.restoreHiddenNodesAfter(async () => {
        layoutStore.mode = GraphMode.tree;
        await layoutStore.updatePositions({});
        layoutStore.setArtifactTreeLayout();
      });
      this.setIsDeltaViewEnabled(true);
    },
    /**
     * Returns the delta states of all of the given artifacts.
     *
     * @param artifactIds - The artifacts to find the state of.
     * @return All unique change states found within the artifacts.
     */
    getArtifactDeltaStates(artifactIds: string[]): ArtifactDeltaState[] {
      const deltaStates = new Set<ArtifactDeltaState>();

      for (const id of artifactIds) {
        if (id in this.projectDelta.artifacts.added) {
          deltaStates.add(ArtifactDeltaState.ADDED);
        } else if (id in this.projectDelta.artifacts.modified) {
          deltaStates.add(ArtifactDeltaState.MODIFIED);
        } else if (id in this.projectDelta.artifacts.removed) {
          deltaStates.add(ArtifactDeltaState.REMOVED);
        }
      }

      return Array.from(deltaStates);
    },

    /**
     * Finds the delta state of a trace link.
     *
     * @param id - The trace link id to find.
     * @return The trace links delta state, if one exists.
     */
    getTraceDeltaType(id: string): ArtifactDeltaState {
      if (!this.inDeltaView) {
        return ArtifactDeltaState.NO_CHANGE;
      } else if (id in this.projectDelta.traces.added) {
        return ArtifactDeltaState.ADDED;
      } else if (id in this.projectDelta.traces.modified) {
        if (
          this.projectDelta.traces.modified[id].after.approvalStatus ===
          ApprovalType.DECLINED
        ) {
          return ArtifactDeltaState.REMOVED;
        } else {
          return ArtifactDeltaState.MODIFIED;
        }
      } else if (id in this.projectDelta.traces.removed) {
        return ArtifactDeltaState.REMOVED;
      } else {
        return ArtifactDeltaState.NO_CHANGE;
      }
    },
    /**
     * Finds the delta state of an artifact.
     *
     * @param id - The artifact id to find.
     * @return The artifact delta state, if one exists.
     */
    getArtifactDeltaType(id: string): ArtifactDeltaState {
      if (!this.inDeltaView) {
        return ArtifactDeltaState.NO_CHANGE;
      } else if (id in this.projectDelta.artifacts.added) {
        return ArtifactDeltaState.ADDED;
      } else if (id in this.projectDelta.artifacts.modified) {
        return ArtifactDeltaState.MODIFIED;
      } else if (id in this.projectDelta.artifacts.removed) {
        return ArtifactDeltaState.REMOVED;
      } else {
        return ArtifactDeltaState.NO_CHANGE;
      }
    },
  },
});

export default useDelta(pinia);
