import { defineStore } from "pinia";

import {
  ArtifactDeltaState,
  ArtifactSchema,
  EntityModificationSchema,
  VersionDeltaSchema,
  TraceLinkSchema,
  VersionSchema,
} from "@/types";
import { buildProjectDelta } from "@/util";
import {
  layoutStore,
  appStore,
  subtreeStore,
  artifactStore,
  traceStore,
  cyStore,
} from "@/hooks";
import { pinia } from "@/plugins";

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
    projectDelta: buildProjectDelta(),
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
    modifiedArtifacts(): Record<
      string,
      EntityModificationSchema<ArtifactSchema>
    > {
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
        layoutStore.mode = "tim";
        this.afterVersion = undefined;
      } else {
        appStore.closeSidePanels();
      }

      this.inDeltaView = isDeltaViewEnabled;

      cyStore.drawMode("disable");
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
     * @param afterVersion - The version that artifact deltas have been made to.
     */
    async setDeltaPayload(
      payload: VersionDeltaSchema,
      afterVersion?: VersionSchema
    ): Promise<void> {
      this.projectDelta = payload;
      this.afterVersion = afterVersion;

      const artifacts = [
        ...Object.values(payload.artifacts.added),
        ...Object.values(payload.artifacts.modified).map(({ after }) => after),
        ...Object.values(payload.artifacts.removed),
      ];

      const removedTraces = Object.values(payload.traces.removed);
      const traces = [
        ...Object.values(payload.traces.added),
        ...Object.values(payload.traces.modified).map(({ after }) => after),
        ...removedTraces,
      ];

      // Add all updated artifacts and traces to the store.
      artifactStore.addOrUpdateArtifacts(artifacts);
      traceStore.addOrUpdateTraceLinks(traces);

      // Add removed traces back into the subtree.
      removedTraces.forEach((trace) => subtreeStore.addTraceSubtree(trace));

      // Switch the current artifact & trace store to only show artifacts in the delta.
      const currentArtifactIds = artifacts.flatMap(({ id }) => [
        id,
        // Add all neighbors of the artifact to the list of artifacts to show.
        ...(subtreeStore.subtreeMap[id]?.neighbors || []),
      ]);

      artifactStore.initializeArtifacts({ currentArtifactIds });
      traceStore.initializeTraces({ currentArtifactIds });

      // Switch to tree view and generate the graph layout for the unique set of delta artifacts.
      await subtreeStore.restoreHiddenNodesAfter(async () => {
        layoutStore.mode = "tree";
        await layoutStore.updatePositions({}, 0);
        layoutStore.setGraphLayout();
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
          deltaStates.add("ADDED");
        } else if (id in this.projectDelta.artifacts.modified) {
          deltaStates.add("MODIFIED");
        } else if (id in this.projectDelta.artifacts.removed) {
          deltaStates.add("REMOVED");
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
        return "NO_CHANGE";
      } else if (id in this.projectDelta.traces.added) {
        return "ADDED";
      } else if (id in this.projectDelta.traces.modified) {
        if (
          this.projectDelta.traces.modified[id].after.approvalStatus ===
          "DECLINED"
        ) {
          return "REMOVED";
        } else {
          return "MODIFIED";
        }
      } else if (id in this.projectDelta.traces.removed) {
        return "REMOVED";
      } else {
        return "NO_CHANGE";
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
        return "NO_CHANGE";
      } else if (id in this.projectDelta.artifacts.added) {
        return "ADDED";
      } else if (id in this.projectDelta.artifacts.modified) {
        return "MODIFIED";
      } else if (id in this.projectDelta.artifacts.removed) {
        return "REMOVED";
      } else {
        return "NO_CHANGE";
      }
    },
  },
});

export default useDelta(pinia);
