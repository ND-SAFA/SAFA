import { defineStore } from "pinia";

import {
  ApprovalType,
  FlatTraceLink,
  GeneratedLinksSchema,
  TraceLinkSchema,
} from "@/types";
import { pinia } from "@/plugins";

/**
 * A module for managing generated trace link approval.
 */
export const useTraceApproval = defineStore("traceApproval", {
  state: () => ({
    /**
     * All generated links.
     */
    traceLinks: [] as FlatTraceLink[],
    /**
     * Approved generated link ids.
     */
    approvedIds: [] as string[],
    /**
     * Declined generated link ids.
     */
    declinedIds: [] as string[],
    /**
     * Expanded generated link ids.
     */
    expandedIds: [] as string[],
  }),
  getters: {
    /**
     * @return All unreviewed links.
     */
    unreviewedLinks(): FlatTraceLink[] {
      return this.traceLinks.filter(
        ({ approvalStatus }) => approvalStatus === "UNREVIEWED"
      );
    },
  },
  actions: {
    /**
     * Initializes the state of generated traces.
     *
     * @param generated - The generated links and their states.
     */
    initializeTraces(generated: GeneratedLinksSchema) {
      this.expandedIds = [];
      this.$patch(generated);
    },
    /**
     * Updates the status of a flat link.
     *
     * @param traceLink - The link to update.
     * @param status - The status to update to.
     */
    updateLinkStatus(traceLink: TraceLinkSchema, status: ApprovalType): void {
      const flatLink = this.traceLinks.find(
        ({ traceLinkId }) => traceLinkId === traceLink.traceLinkId
      );

      if (!flatLink) return;

      flatLink.approvalStatus = status;
    },
    /**
     * Deselects a link.
     *
     * @param traceLinkId - The link id to deselect.
     */
    deselectLink(traceLinkId: string) {
      this.expandedIds = this.expandedIds.filter((id) => id !== traceLinkId);
    },
    /**
     * Updates the stored links with a new approved status.
     *
     * @param traceLink - The link to approve.
     */
    approveLink(traceLink: TraceLinkSchema): void {
      this.declinedIds = this.declinedIds.filter(
        (declinedId) => declinedId != traceLink.traceLinkId
      );
      this.approvedIds = [...this.approvedIds, traceLink.traceLinkId];
      this.deselectLink(traceLink.traceLinkId);
      this.updateLinkStatus(traceLink, "APPROVED");
    },
    /**
     * Updates the stored links with a new declined status.
     *
     * @param traceLink - The link to decline.
     */
    declineLink(traceLink: TraceLinkSchema): void {
      this.approvedIds = this.approvedIds.filter(
        (approvedId) => approvedId != traceLink.traceLinkId
      );
      this.declinedIds = [...this.declinedIds, traceLink.traceLinkId];
      this.deselectLink(traceLink.traceLinkId);
      this.updateLinkStatus(traceLink, "DECLINED");
    },
    /**
     * Updates the stored links with a new un-reviewed status.
     *
     * @param traceLink - The link to reset.
     */
    resetLink(traceLink: TraceLinkSchema): void {
      this.approvedIds = this.approvedIds.filter(
        (approvedId) => approvedId != traceLink.traceLinkId
      );
      this.declinedIds = this.declinedIds.filter(
        (declinedId) => declinedId != traceLink.traceLinkId
      );
      this.deselectLink(traceLink.traceLinkId);
      this.updateLinkStatus(traceLink, "UNREVIEWED");
    },
    /**
     * Expands all matching links.
     * @param filter - The filter to select which links to expand.
     */
    expandLinks(filter: (traceLink: FlatTraceLink) => boolean): void {
      this.expandedIds = this.traceLinks
        .filter(filter)
        .map((link) => link.traceLinkId);
    },
    /**
     * Collapses all matching links.
     * @param filter - The filter to select which links to preserve.
     */
    collapseLinks(filter: (traceLink: FlatTraceLink) => boolean): void {
      this.expandedIds = this.traceLinks
        .filter(
          (link) => this.expandedIds.includes(link.traceLinkId) && filter(link)
        )
        .map((link) => link.traceLinkId);
    },
  },
});

export default useTraceApproval(pinia);
