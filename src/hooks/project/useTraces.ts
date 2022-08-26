import { defineStore } from "pinia";

import {
  ApprovalType,
  ArtifactData,
  ArtifactModel,
  DocumentTraces,
  TraceLinkModel,
} from "@/types";
import { matchTrace, removeMatches, standardizeValueArray } from "@/util";
import { pinia } from "@/plugins";
import documentStore from "@/hooks/project/useDocuments";
import subtreeStore from "@/hooks/project/useSubtree";
import layoutStore from "@/hooks/graph/useLayout";
import projectStore from "@/hooks/project/useProject";
import typeOptionsStore from "@/hooks/project/useTypeOptions";

/**
 * This module defines the state of the current project's trace links.
 */
export const useTraces = defineStore("traces", {
  state: () => ({
    /**
     * All trace links in the project.
     */
    allTraces: [] as TraceLinkModel[],
    /**
     * The visible trace links.
     */
    currentTraces: [] as TraceLinkModel[],
  }),
  getters: {
    /**
     * @return All visible trace links.
     */
    visibleTraces(): TraceLinkModel[] {
      return this.currentTraces.filter(
        (t) => t.approvalStatus != ApprovalType.DECLINED
      );
    },
  },
  actions: {
    /**
     * Initializes the trace links visible in the current document.
     */
    initializeTraces(documentTraces: DocumentTraces): void {
      const { traces = this.allTraces, currentArtifactIds } = documentTraces;

      this.$patch({
        allTraces: traces,
        currentTraces: currentArtifactIds
          ? traces.filter(
              ({ sourceId, targetId }) =>
                currentArtifactIds.includes(sourceId) &&
                currentArtifactIds.includes(targetId)
            )
          : traces,
      });
    },
    /**
     * Updates the current trace links in the project, preserving any that already existed.
     *
     * @param newTraces - The trace links to add.
     */
    addOrUpdateTraceLinks(newTraces: TraceLinkModel[]): void {
      const newIds = newTraces.map(({ traceLinkId }) => traceLinkId);
      const updatedTraces = [
        ...removeMatches(this.allTraces, "traceLinkId", newIds),
        ...newTraces,
      ];

      this.initializeTraces({
        traces: updatedTraces,
        currentArtifactIds: documentStore.currentDocument.artifactIds,
      });
      projectStore.updateProject({ traces: updatedTraces });
      subtreeStore.updateSubtreeMap();
      layoutStore.applyAutomove();
    },
    /**
     * Deletes the given trace links.
     *
     * @param deletedTraces - The trace links, or ids, to remove.
     */
    async deleteTraceLinks(
      deletedTraces: TraceLinkModel[] | string[]
    ): Promise<void> {
      if (deletedTraces.length === 0) return;

      const ids = standardizeValueArray(deletedTraces, "traceLinkId");
      const allTraces = removeMatches(this.allTraces, "traceLinkId", ids);

      this.$patch({
        allTraces,
        currentTraces: removeMatches(this.currentTraces, "traceLinkId", ids),
      });
      projectStore.updateProject({ traces: allTraces });
      subtreeStore.updateSubtreeMap();
      layoutStore.applyAutomove();
    },
    /**
     * Returns the trace link between artifacts.
     *
     * @param sourceId - The source artifact id.
     * @param targetId - The target artifact id.
     * @return The trace link between artifacts, if one exists.
     */
    getTraceLinkByArtifacts(
      sourceId: string,
      targetId: string
    ): TraceLinkModel | undefined {
      return this.allTraces.find(matchTrace(sourceId, targetId));
    },
    /**
     * Returns whether the link exists.
     *
     * @param sourceId - The source artifact id.
     * @param targetId - The target artifact id.
     * @return Whether a link exists.
     */
    doesLinkExist(sourceId: string, targetId: string): boolean {
      return !!this.allTraces.find(matchTrace(sourceId, targetId, true));
    },
    /**
     * Returns whether the link is allowed.
     *
     * @param source - The source artifact.
     * @param target - The target artifact.
     * @return Whether a link can be created, or a reason why it cant.
     */
    isLinkAllowed(
      source: ArtifactModel | ArtifactData,
      target: ArtifactModel | ArtifactData
    ): string | boolean {
      if (source.id === target.id) {
        return "An artifact cannot link to itself.";
      } else if (
        this.doesLinkExist(source.id, target.id) ||
        this.doesLinkExist(target.id, source.id)
      ) {
        return "This trace link already exists.";
      } else if (!typeOptionsStore.isLinkAllowedByType(source, target)) {
        return `The type "${source.type}" cannot trace to "${target.type}".`;
      }

      return true;
    },
  },
});

export default useTraces(pinia);
