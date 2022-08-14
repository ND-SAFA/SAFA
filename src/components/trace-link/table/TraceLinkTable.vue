<template>
  <v-container>
    <v-data-table
      class="trace-link-table"
      show-group-by
      show-expand
      single-expand
      multi-sort
      :headers="headers"
      :items="items"
      :expanded="expanded"
      :search="searchText"
      :loading="isLoading"
      :sort-by="['targetName', 'sourceName']"
      :group-desc="true"
      group-by="approvalStatus"
      item-key="traceLinkId"
      :items-per-page="50"
      @click:row="handleView($event)"
    >
      <template v-slot:top>
        <trace-link-table-header
          @search="searchText = $event"
          @open:all="handleOpenAll"
          @close:all="handleCloseAll"
        />
      </template>

      <template v-slot:[`group.header`]="data">
        <table-group-header :data="data" />
      </template>

      <template v-slot:[`item.sourceType`]="{ item, header }">
        <td class="v-data-table__divider">
          <attribute-chip :value="item.sourceType" artifact-type />
        </td>
      </template>

      <template v-slot:[`item.targetType`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip :value="item.targetType" artifact-type />
        </td>
      </template>

      <template v-slot:[`item.approvalStatus`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip :value="item.approvalStatus" />
        </td>
      </template>

      <template v-slot:[`item.score`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip confidence-score :value="String(item.score)" />
        </td>
      </template>

      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length" class="pb-2">
          <trace-link-display
            :link="item"
            @link:approve="handleApprove($event)"
            @link:decline="handleDecline($event)"
            @link:unreview="handleUnreview($event)"
          />
        </td>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { ApprovalType, TraceLinkModel, VersionModel } from "@/types";
import { appModule, artifactModule, projectModule } from "@/store";
import { getGeneratedLinks } from "@/api";
import { AttributeChip, TableGroupHeader } from "@/components/common";
import TraceLinkDisplay from "../TraceLinkDisplay.vue";
import TraceLinkTableHeader from "./TraceLinkTableHeader.vue";

/**
 * Displays a table of trace links.
 */
export default Vue.extend({
  name: "TraceLinkTable",
  components: {
    TableGroupHeader,
    TraceLinkTableHeader,
    AttributeChip,
    TraceLinkDisplay,
  },
  data() {
    return {
      searchText: "",
      headers: [
        {
          text: "Source Name",
          value: "sourceName",
          filterable: true,
        },
        {
          text: "Source Type",
          value: "sourceType",
          filterable: true,
          divider: true,
        },
        {
          text: "Target Name",
          value: "targetName",
          filterable: true,
        },
        {
          text: "Target Type",
          value: "targetType",
          filterable: true,
          divider: true,
        },
        {
          text: "Approval Status",
          value: "approvalStatus",
          filterable: true,
          divider: true,
        },
        {
          text: "Confidence Score",
          value: "score",
          groupable: false,
          divider: true,
        },
        {
          value: "data-table-expand",
          groupable: false,
        },
      ],
      links: [] as TraceLinkModel[],
      expanded: [] as TraceLinkModel[],
      approved: [] as string[],
      declined: [] as string[],
    };
  },
  mounted() {
    this.loadGeneratedLinks();
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
     * @return Whether the app is loading.
     */
    isLoading() {
      return appModule.getIsLoading;
    },
    /**
     * @return The current project version.
     */
    projectVersion() {
      return projectModule.getProject.projectVersion;
    },
    items(): TraceLinkModel[] {
      return this.links.map((link) => ({
        ...link,
        sourceType: artifactModule.getArtifactById(link.sourceId).type,
        targetType: artifactModule.getArtifactById(link.targetId).type,
      }));
    },
  },
  methods: {
    /**
     * Loads the generated links for the current project.
     */
    async loadGeneratedLinks() {
      try {
        appModule.onLoadStart();
        const versionId = projectModule.versionIdWithLog;
        this.links = await getGeneratedLinks(versionId);
        this.approved = [];
        this.declined = [];
        this.expanded = [];

        this.links.forEach((link) => {
          if (link.approvalStatus === ApprovalType.APPROVED) {
            this.approved.push(link.traceLinkId);
          } else if (link.approvalStatus === ApprovalType.DECLINED) {
            this.declined.push(link.traceLinkId);
          }
        });
      } finally {
        appModule.onLoadEnd();
      }
    },
    /**
     * Opens all panels.
     */
    handleOpenAll() {
      this.expanded = this.links;
    },
    /**
     * Closes all panels.
     */
    handleCloseAll() {
      this.expanded = [];
    },
    /**
     * Approves the given link and updates the stored links.
     *
     * @param link - The link to approve.
     */
    handleApprove(link: TraceLinkModel) {
      this.declined = this.declined.filter(
        (declinedId) => declinedId != link.traceLinkId
      );
      this.approved.push(link.traceLinkId);
    },
    /**
     * Declines the given link and updates the stored links.
     *
     * @param link - The link to decline.
     */
    handleDecline(link: TraceLinkModel) {
      this.approved = this.approved.filter(
        (declinedId) => declinedId != link.traceLinkId
      );
      this.declined.push(link.traceLinkId);
    },
    /**
     * Unreivews the given link and updates the stored links.
     *
     * @param link - The link to unreview.
     */
    handleUnreview(link: TraceLinkModel) {
      this.approved = this.approved.filter(
        (declinedId) => declinedId != link.traceLinkId
      );
      this.declined = this.declined.filter(
        (declinedId) => declinedId != link.traceLinkId
      );
    },
    /**
     * Handles viewing a trace link.
     *
     * @param link - The link to view.
     */
    handleView(link: TraceLinkModel) {
      if (this.expanded.includes(link)) {
        this.expanded = this.expanded.filter(
          (expandedLink) => link.traceLinkId !== expandedLink.traceLinkId
        );
      } else {
        this.expanded = [...this.expanded, link];
      }
    },
  },
});
</script>

<style scoped></style>
