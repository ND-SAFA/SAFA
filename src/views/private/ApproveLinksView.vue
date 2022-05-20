<template>
  <private-page>
    <template v-slot:page>
      <v-btn text @click="handleGoBack">
        <v-icon left> mdi-arrow-left </v-icon>
        Back To Tree View
      </v-btn>
      <approval-section
        show-approve
        show-decline
        title="Un-Reviewed Trace Links"
        :links="links"
        :artifacts="artifactsById"
        @link:approve="handleApprove"
        @link:decline="handleDecline"
      />
      <approval-section
        show-approve
        title="Declined Trace Links"
        :show-decline="false"
        :start-open="false"
        :links="declinedLinks"
        :artifacts="artifactsById"
        @link:approve="handleApproveDeclined"
      />
      <approval-section
        show-decline
        title="Approved Trace Links"
        :show-approve="false"
        :start-open="false"
        :links="approvedLinks"
        :artifacts="artifactsById"
        @link:decline="handleDeclineApproved"
      />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { TraceApproval, TraceLink, ProjectVersion, EmptyLambda } from "@/types";
import { navigateBack } from "@/router";
import { artifactModule, projectModule } from "@/store";
import { handleApproveLink, handleDeclineLink, getGeneratedLinks } from "@/api";
import { ApprovalSection, PrivatePage } from "@/components";

export default Vue.extend({
  name: "ApproveLinksView",
  components: { PrivatePage, ApprovalSection },
  data() {
    return {
      links: [] as TraceLink[],
      declinedLinks: [] as TraceLink[],
      approvedLinks: [] as TraceLink[],
    };
  },
  watch: {
    /**
     * Loads generated links when the version changes.
     */
    projectVersion(newVersion?: ProjectVersion) {
      if (!newVersion) return;

      this.loadGeneratedLinks();
    },
  },
  computed: {
    /**
     * @return A collection of all artifacts, keyed by their id.
     */
    artifactsById() {
      return artifactModule.getArtifactsById;
    },
    /**
     * @return The current project version.
     */
    projectVersion() {
      return projectModule.getProject.projectVersion;
    },
  },
  methods: {
    /**
     * Navigates back to the artifact page.
     */
    handleGoBack() {
      navigateBack();
    },

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
          case TraceApproval.UNREVIEWED:
            this.links.push(link);
            break;
          case TraceApproval.APPROVED:
            this.approvedLinks.push(link);
            break;
          case TraceApproval.DECLINED:
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
    approveLink(link: TraceLink, filterCallback: EmptyLambda) {
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
    declineLink(link: TraceLink, filterCallback: EmptyLambda) {
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
    handleApprove(link: TraceLink) {
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
    handleApproveDeclined(link: TraceLink) {
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
    handleDecline(link: TraceLink) {
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
    handleDeclineApproved(link: TraceLink) {
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
