<template>
  <private-page>
    <template v-slot:page>
      <back-button text="Back To Tree View" />
      <trace-link-table />
      <approval-section
        show-approve
        show-decline
        title="Un-Reviewed Trace Links"
        :links="links"
        @link:approve="handleApprove"
        @link:decline="handleDecline"
      />
      <approval-section
        show-approve
        :show-decline="false"
        title="Declined Trace Links"
        :start-open="false"
        :links="declinedLinks"
        @link:approve="handleApproveDeclined"
      />
      <approval-section
        show-decline
        :show-approve="false"
        title="Approved Trace Links"
        :start-open="false"
        :links="approvedLinks"
        @link:decline="handleDeclineApproved"
      />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import {
  ApprovalType,
  TraceLinkModel,
  VersionModel,
  EmptyLambda,
} from "@/types";
import { projectModule } from "@/store";
import { handleApproveLink, handleDeclineLink, getGeneratedLinks } from "@/api";
import {
  ApprovalSection,
  PrivatePage,
  BackButton,
  TraceLinkTable,
} from "@/components";

export default Vue.extend({
  name: "ApproveLinksView",
  components: { TraceLinkTable, BackButton, PrivatePage, ApprovalSection },
  data() {
    return {
      links: [] as TraceLinkModel[],
      declinedLinks: [] as TraceLinkModel[],
      approvedLinks: [] as TraceLinkModel[],
    };
  },
  watch: {
    /**
     * Loads generated links when the version changes.
     */
    projectVersion(newVersion?: VersionModel) {
      if (!newVersion) return;

      this.loadGeneratedLinks();
    },
  },
  computed: {
    /**
     * @return The current project version.
     */
    projectVersion() {
      return projectModule.getProject.projectVersion;
    },
  },
  methods: {
    /**
     * Loads the generated links for the current project.
     */
    async loadGeneratedLinks() {
      const versionId = projectModule.versionIdWithLog;
      const links = await getGeneratedLinks(versionId);

      this.links = [];
      this.approvedLinks = [];
      this.declinedLinks = [];

      links.forEach((link) => {
        switch (link.approvalStatus) {
          case ApprovalType.UNREVIEWED:
            this.links.push(link);
            break;
          case ApprovalType.APPROVED:
            this.approvedLinks.push(link);
            break;
          case ApprovalType.DECLINED:
            this.declinedLinks.push(link);
            break;
        }
      });
    },

    /**
     * Approves the given link.
     *
     * @param link - The link to approve.
     * @param filterCallback - The callback to run afterward.
     */
    approveLink(link: TraceLinkModel, filterCallback: EmptyLambda) {
      handleApproveLink(link, () => {
        filterCallback();
        this.approvedLinks = this.approvedLinks.concat([link]);
      });
    },
    /**
     * Declines the given link.
     *
     * @param link - The link to decline.
     * @param filterCallback - The callback to run afterward.
     */
    declineLink(link: TraceLinkModel, filterCallback: EmptyLambda) {
      handleDeclineLink(link, () => {
        filterCallback();
        this.declinedLinks = this.declinedLinks.concat([link]);
      });
    },

    /**
     * Approves the given link and updates the stored links.
     *
     * @param link - The link to approve.
     */
    handleApprove(link: TraceLinkModel) {
      this.approveLink(link, () => {
        this.links = this.links.filter(
          (t) => t.traceLinkId != link.traceLinkId
        );
      });
    },
    /**
     * Approves the given declined link and updates the stored links.
     *
     * @param link - The link to approve.
     */
    handleApproveDeclined(link: TraceLinkModel) {
      this.approveLink(link, () => {
        this.declinedLinks = this.declinedLinks.filter(
          (t) => t.traceLinkId != link.traceLinkId
        );
      });
    },
    /**
     * Declines the given link and updates the stored links.
     *
     * @param link - The link to decline.
     */
    handleDecline(link: TraceLinkModel) {
      this.declineLink(link, () => {
        this.links = this.links.filter(
          (t) => t.traceLinkId != link.traceLinkId
        );
      });
    },
    /**
     * Declines the given approved link and updates the stored links.
     *
     * @param link - The link to decline.
     */
    handleDeclineApproved(link: TraceLinkModel) {
      this.declineLink(link, () => {
        this.approvedLinks = this.approvedLinks.filter(
          (t) => t.traceLinkId != link.traceLinkId
        );
      });
    },
  },
  mounted() {
    this.loadGeneratedLinks();
  },
});
</script>
