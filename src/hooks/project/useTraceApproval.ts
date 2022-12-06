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
     * All links that are selected.
     */
    selectedLinks: [] as FlatTraceLink[],
    /**
     * Approved generated link ids.
     */
    approvedIds: [] as string[],
    /**
     * Declined generated link ids.
     */
    declinedIds: [] as string[],
  }),
  getters: {
    /**
     * @return All unreviewed links.
     */
    unreviewedLinks(): FlatTraceLink[] {
      return this.traceLinks.filter(
        ({ approvalStatus }) => approvalStatus === ApprovalType.UNREVIEWED
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
      this.selectedLinks = [];
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
     * Selects all links that meet the filter predicate.
     *
     * @param filter - The filter to run on all links.
     */
    selectLinks(filter: (link: FlatTraceLink) => boolean) {
      this.selectedLinks = this.traceLinks.filter(filter);
    },
    /**
     * Deselects all links that meet the filter predicate.
     *
     * @param filter - The filter to run on selected links.
     */
    deselectLinks(filter: (link: FlatTraceLink) => boolean) {
      this.selectedLinks = this.selectedLinks.filter(filter);
    },
    /**
     * Toggles the selected state of a link.
     *
     * @param traceLink - The link to toggle.
     */
    toggleLink(traceLink: FlatTraceLink) {
      if (this.selectedLinks.includes(traceLink)) {
        this.deselectLinks(
          ({ traceLinkId }) => traceLinkId !== traceLink.traceLinkId
        );
      } else {
        this.selectedLinks = [...this.selectedLinks, traceLink];
      }
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
      this.deselectLinks(
        ({ traceLinkId }) => traceLinkId !== traceLink.traceLinkId
      );
      this.updateLinkStatus(traceLink, ApprovalType.APPROVED);
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
      this.deselectLinks(
        ({ traceLinkId }) => traceLinkId !== traceLink.traceLinkId
      );
      this.updateLinkStatus(traceLink, ApprovalType.DECLINED);
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
      this.deselectLinks(
        ({ traceLinkId }) => traceLinkId !== traceLink.traceLinkId
      );
      this.updateLinkStatus(traceLink, ApprovalType.UNREVIEWED);
    },
  },
});

export default useTraceApproval(pinia);
