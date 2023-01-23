import { defineStore } from "pinia";

import {
  ApprovalType,
  ArtifactCytoElementData,
  ArtifactSchema,
  DocumentTraces,
  TraceLinkSchema,
  TraceType,
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
    allTraces: [] as TraceLinkSchema[],
    /**
     * The visible trace links.
     */
    currentTraces: [] as TraceLinkSchema[],
  }),
  getters: {
    /**
     * @return All visible trace links.
     */
    visibleTraces(): TraceLinkSchema[] {
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
    addOrUpdateTraceLinks(newTraces: TraceLinkSchema[]): void {
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
      typeOptionsStore.updateTIM();
      layoutStore.applyAutomove();
    },
    /**
     * Deletes the given trace links.
     *
     * @param deletedTraces - The trace links, or ids, to remove.
     */
    async deleteTraceLinks(
      deletedTraces: TraceLinkSchema[] | string[]
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
      typeOptionsStore.updateTIM();
      layoutStore.applyAutomove();
    },
    /**
     * Returns the trace link that matches an id.
     *
     * @param id - The trace link id.
     * @return The trace link, if one exists.
     */
    getTraceLinkById(id: string): TraceLinkSchema | undefined {
      return this.allTraces.find(({ traceLinkId }) => traceLinkId === id);
    },
    /**
     * Returns the trace link between artifacts.
     *
     * @param sourceId - The source artifact id.
     * @param targetId - The target artifact id.
     * @param ignoreDirection - If true, will match traces in both directions.
     * @return The trace link between artifacts, if one exists.
     */
    getTraceLinkByArtifacts(
      sourceId: string,
      targetId: string,
      ignoreDirection = false
    ): TraceLinkSchema | undefined {
      return this.allTraces.find(
        matchTrace(sourceId, targetId, ignoreDirection)
      );
    },
    /**
     * Returns the trace link between sets of artifacts.
     *
     * @param sources - The source artifacts.
     * @param targets - The target artifacts.
     * @param filters - Whether to additionally filter by manual or approved links.
     * @return All trace links from source to target artifacts.
     */
    getTraceLinksByArtifactSets(
      sources: ArtifactSchema[],
      targets: ArtifactSchema[],
      filters: ("manual" | "approved")[] = []
    ): TraceLinkSchema[] {
      const linksBetweenSets = this.allTraces.filter(
        ({ sourceId, targetId }) =>
          !!sources.find(({ id }) => id === sourceId) &&
          !!targets.find(({ id }) => id === targetId)
      );

      if (filters.includes("manual") && filters.includes("approved")) {
        return linksBetweenSets.filter(
          ({ approvalStatus }) => approvalStatus === ApprovalType.APPROVED
        );
      } else if (filters.includes("manual")) {
        return linksBetweenSets.filter(
          ({ traceType }) => traceType === TraceType.MANUAL
        );
      } else if (filters.includes("approved")) {
        return linksBetweenSets.filter(
          ({ traceType, approvalStatus }) =>
            traceType === TraceType.GENERATED &&
            approvalStatus === ApprovalType.APPROVED
        );
      } else {
        return linksBetweenSets;
      }
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
      source: ArtifactSchema | ArtifactCytoElementData,
      target: ArtifactSchema | ArtifactCytoElementData
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
