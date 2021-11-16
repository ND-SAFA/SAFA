<template>
  <private-page>
    <template v-slot:page>
      <v-row justify="center">
        <ApprovalSection
          title="Un-Reviewed Trace Links"
          :showApprove="true"
          :showDecline="true"
          :links="links"
          :artifacts="artifactHashmap"
          @approve-link="onApproveLink"
          @decline-link="onDeclineLink"
        />
      </v-row>
      <v-row justify="center">
        <ApprovalSection
          showApprove
          title="Declined Trace Links"
          :showDecline="false"
          :startOpen="false"
          :links="declinedLinks"
          :artifacts="artifactHashmap"
          @approve-link="onApproveDeclinedLink"
        />
      </v-row>
      <v-row justify="center">
        <ApprovalSection
          showDecline
          title="Approved Trace Links"
          :showApprove="false"
          :startOpen="false"
          :links="approvedLinks"
          :artifacts="artifactHashmap"
          @decline-link="onDeclineApprovedLink"
        />
      </v-row>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import {
  approveLinkAPIHandler,
  declineLinkAPIHandler,
  getGeneratedLinks,
} from "@/api";
import { TraceApproval, TraceLink, Artifact } from "@/types/domain";
import { appModule, projectModule } from "@/store";
import { ApprovalSection, PrivatePage } from "@/components";

export default Vue.extend({
  name: "approval-links-view",
  components: { PrivatePage, ApprovalSection },
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
