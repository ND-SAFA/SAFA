import { defineStore } from "pinia";

import {
  ArtifactCytoElementData,
  ArtifactSchema,
  DocumentTraces,
  TraceLinkSchema,
} from "@/types";
import {
  getTraceId,
  matchTrace,
  removeMatches,
  standardizeValueArray,
} from "@/util";
import { timStore, layoutStore, selectionStore } from "@/hooks";
import { pinia } from "@/plugins";

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
    /**
     * A map of trace links by artifact ids.
     */
    tracesById: new Map<string, TraceLinkSchema>(),
  }),
  getters: {
    /**
     * @return All visible trace links.
     */
    visibleTraces(): TraceLinkSchema[] {
      return this.currentTraces.filter((t) => t.approvalStatus != "DECLINED");
    },
    /**
     * @return The currently selected trace link.
     */
    selectedTraceLink(): TraceLinkSchema | undefined {
      return this.tracesById.get(
        getTraceId(
          selectionStore.selectedTraceLinkIds[0],
          selectionStore.selectedTraceLinkIds[1]
        )
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
        tracesById: new Map(
          traces.map((trace) => [
            getTraceId(trace.sourceId, trace.targetId),
            trace,
          ])
        ),
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

      this.$patch({
        allTraces: updatedTraces,
        currentTraces: [
          ...removeMatches(this.currentTraces, "traceLinkId", newIds),
          ...newTraces,
        ],
        tracesById: new Map(
          updatedTraces.map((trace) => [
            getTraceId(trace.sourceId, trace.targetId),
            trace,
          ])
        ),
      });
      layoutStore.applyAutomove();
    },
    /**
     * Deletes the given trace links.
     *
     * @param deletedTraces - The trace links, or ids, to remove.
     */
    deleteTraceLinks(deletedTraces: TraceLinkSchema[] | string[]): void {
      if (deletedTraces.length === 0) return;

      const ids = standardizeValueArray(deletedTraces, "traceLinkId");
      const allTraces = removeMatches(this.allTraces, "traceLinkId", ids);

      this.$patch({
        allTraces,
        currentTraces: removeMatches(this.currentTraces, "traceLinkId", ids),
        tracesById: new Map(
          allTraces.map((trace) => [
            getTraceId(trace.sourceId, trace.targetId),
            trace,
          ])
        ),
      });
      layoutStore.applyAutomove();
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
      return ignoreDirection
        ? this.tracesById.get(getTraceId(sourceId, targetId)) ||
            this.tracesById.get(getTraceId(targetId, sourceId))
        : this.tracesById.get(getTraceId(sourceId, targetId));
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
          ({ approvalStatus }) => approvalStatus === "APPROVED"
        );
      } else if (filters.includes("manual")) {
        return linksBetweenSets.filter(
          ({ traceType }) => traceType === "MANUAL"
        );
      } else if (filters.includes("approved")) {
        return linksBetweenSets.filter(
          ({ traceType, approvalStatus }) =>
            traceType === "GENERATED" && approvalStatus === "APPROVED"
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
      source: ArtifactSchema | ArtifactCytoElementData | undefined,
      target: ArtifactSchema | ArtifactCytoElementData | undefined
    ): string | boolean {
      if (!source || !target) {
        return false;
      } else if (source.id === target.id) {
        return "An artifact cannot link to itself.";
      } else if (
        this.doesLinkExist(source.id, target.id) ||
        this.doesLinkExist(target.id, source.id)
      ) {
        return "This trace link already exists.";
      } else if (!timStore.canBeTraced(source, target)) {
        return `The type "${source.type}" cannot trace to "${target.type}".`;
      }

      return true;
    },
  },
});

export default useTraces(pinia);
