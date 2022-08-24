import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import {
  ApprovalType,
  ArtifactData,
  ArtifactModel,
  DocumentTraces,
  TraceLinkModel,
} from "@/types";
import typeOptionsStore from "./useTypeOptions";

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
     * DO NOT CALL THIS OUTSIDE OF THE STORES.
     * Deletes the given trace links.
     *
     * @param deletedIds - The trace link ids to remove.
     */
    async deleteTraceLinks(deletedIds: string[]): Promise<void> {
      const removeLink = (currentTraces: TraceLinkModel[]) =>
        currentTraces.filter(
          ({ traceLinkId }) => !deletedIds.includes(traceLinkId)
        );

      this.$patch({
        allTraces: removeLink(this.allTraces),
        currentTraces: removeLink(this.currentTraces),
      });
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
      return this.allTraces.find(
        (trace) => trace.sourceId === sourceId && trace.targetId === targetId
      );
    },
    /**
     * Returns whether the link exists.
     *
     * @param sourceId - The source artifact id.
     * @param targetId - The target artifact id.
     * @return Whether a link exists.
     */
    doesLinkExist(
      sourceId: string,
      targetId: string
    ): TraceLinkModel | undefined {
      return this.allTraces.find(
        (trace) =>
          (trace.sourceId === sourceId && trace.targetId === targetId) ||
          (trace.targetId === sourceId && trace.sourceId === targetId)
      );
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
