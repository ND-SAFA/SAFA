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
        :artifacts="artifactHashmap"
        @link:approve="onApproveLink"
        @link:decline="onDeclineLink"
      />
      <v-divider class="mt-5" />
      <approval-section
        show-approve
        title="Declined Trace Links"
        :show-decline="false"
        :start-open="false"
        :links="declinedLinks"
        :artifacts="artifactHashmap"
        @link:approve="onApproveDeclinedLink"
      />
      <v-divider class="mt-5" />
      <approval-section
        show-decline
        title="Approved Trace Links"
        :show-approve="false"
        :start-open="false"
        :links="approvedLinks"
        :artifacts="artifactHashmap"
        @link:decline="onDeclineApprovedLink"
      />
      <v-divider class="mt-5 mb-10" />
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
import { artifactModule, logModule, projectModule } from "@/store";
import { ApprovalSection, PrivatePage } from "@/components";
import { navigateTo, Routes } from "@/router";
import { EmptyLambda } from "@/types";

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
      return projectModule.projectId;
    },
    artifactHashmap(): Record<string, Artifact> {
      return artifactModule.getArtifactsById;
    },
  },
  methods: {
    handleGoBack() {
      navigateTo(Routes.ARTIFACT_TREE);
    },
    loadGeneratedLinks() {
      const versionId = projectModule.versionId;

      if (!versionId) {
        return logModule.onWarning("No project has been selected");
      }

      getGeneratedLinks(versionId).then((links) => {
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
    approveLinkHandler(link: TraceLink, filterCallback: EmptyLambda) {
      approveLinkAPIHandler(link, () => {
        filterCallback();
        this.approvedLinks = this.approvedLinks.concat([link]);
      });
    },
    declineLinkHandler(link: TraceLink, filterCallback: EmptyLambda) {
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
