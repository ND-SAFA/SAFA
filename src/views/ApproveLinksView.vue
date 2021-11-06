<template>
  <v-container>
    <v-row justify="center">
      <ApprovalSection
        title="Un-Reviewed Trace Links"
        :showApprove="true"
        :showDecline="true"
        :links="links"
        :artifacts="artifactHashmap"
        @approveLink="onApproveLink"
        @declineLink="onDeclineLink"
      />
    </v-row>
    <v-row justify="center">
      <ApprovalSection
        title="Declined Trace Links"
        :showApprove="true"
        :showDecline="false"
        :links="declinedLinks"
        :artifacts="artifactHashmap"
        @approveLink="onApproveDeclinedLink"
        :startOpen="false"
      />
    </v-row>
    <v-row justify="center">
      <ApprovalSection
        title="Approved Trace Links"
        :showApprove="false"
        :showDecline="true"
        :links="approvedLinks"
        :artifacts="artifactHashmap"
        @declineLink="onDeclineApprovedLink"
        :startOpen="false"
      />
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import {
  approveLinkAPIHandler,
  declineLinkAPIHandler,
  getGeneratedLinks,
} from "@/api";
import ApprovalSection from "@/components/approve-links-view/ApprovalSection.vue";
import { TraceApproval, TraceLink, Artifact } from "@/types";
import { appModule, projectModule } from "@/store";

export default Vue.extend({
  components: { ApprovalSection },
  name: "trace-link-approval",
  data() {
    return {
      links: [] as TraceLink[],
      declinedLinks: [] as TraceLink[],
      approvedLinks: [] as TraceLink[],
    };
  },
  computed: {
    projectId(): string {
      return projectModule.getProject.projectId;
    },
    artifactHashmap(): Record<string, Artifact> {
      return projectModule.getArtifactHashmap;
    },
  },
  methods: {
    loadGeneratedLinks() {
      if (this.projectId === "") {
        return appModule.onWarning("No project has been selected");
      }
      getGeneratedLinks(this.projectId).then((links) => {
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
      });
    },
    approveLinkHandler(link: TraceLink, filterCallback: () => void) {
      approveLinkAPIHandler(link, () => {
        filterCallback();
        this.approvedLinks = this.approvedLinks.concat([link]);
      });
    },
    declineLinkHandler(link: TraceLink, filterCallback: () => void) {
      declineLinkAPIHandler(link, () => {
        filterCallback();
        this.declinedLinks = this.declinedLinks.concat([link]);
      });
    },
    // methods directly used in component
    onApproveLink(link: TraceLink) {
      this.approveLinkHandler(link, () => {
        this.links = this.links.filter(
          (t) => t.traceLinkId != link.traceLinkId
        );
      });
    },
    onApproveDeclinedLink(link: TraceLink) {
      this.approveLinkHandler(link, () => {
        this.declinedLinks = this.declinedLinks.filter(
          (t) => t.traceLinkId != link.traceLinkId
        );
      });
    },
    onDeclineLink(link: TraceLink) {
      this.declineLinkHandler(link, () => {
        this.links = this.links.filter(
          (t) => t.traceLinkId != link.traceLinkId
        );
      });
    },
    onDeclineApprovedLink(link: TraceLink) {
      this.declineLinkHandler(link, () => {
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
