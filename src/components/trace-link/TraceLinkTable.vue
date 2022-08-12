<template>
  <v-container>
    <v-data-table
      class="trace-link-table"
      show-group-by
      show-expand
      single-expand
      fixed-header
      :headers="headers"
      :items="items"
      :expanded="expanded"
      :search="searchText"
      sort-by="targetName"
      item-key="traceLinkId"
      :items-per-page="50"
      @click:row="handleView($event)"
    >
      <template v-slot:top>
        <flex-box justify="space-between">
          <v-text-field
            dense
            outlined
            clearable
            label="Search Trace Links"
            style="max-width: 600px"
            v-model="searchText"
            append-icon="mdi-magnify"
          />
          <section-controls
            @open:all="handleOpenAll"
            @close:all="handleCloseAll"
          />
        </flex-box>
      </template>

      <template v-slot:[`item.sourceType`]="{ item }">
        <td>
          <table-chip :text="item.sourceType" display-icon />
        </td>
      </template>

      <template v-slot:[`item.targetType`]="{ item }">
        <td>
          <table-chip :text="item.targetType" display-icon />
        </td>
      </template>

      <template v-slot:[`item.approvalStatus`]="{ item }">
        <td>
          <approval-chip :link="item" />
        </td>
      </template>

      <template v-slot:[`item.score`]="{ item }">
        <td>
          <typography :value="String(item.score).slice(0, 4)" />
        </td>
      </template>

      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length" class="pb-2">
          <trace-link-display
            :link="item"
            :show-decline="showDeclined(item)"
            :show-approve="showApproved(item)"
            :show-delete="false"
            @link:approve="handleApprove($event)"
            @link:decline="handleDecline($event)"
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
import { FlexBox, TableChip, Typography } from "@/components/common";
import TraceLinkDisplay from "./TraceLinkDisplay.vue";
import SectionControls from "./SectionControls.vue";
import ApprovalChip from "./ApprovalChip.vue";

/**
 * Displays a table of trace links.
 */
export default Vue.extend({
  name: "TraceLinkTable",
  components: {
    Typography,
    ApprovalChip,
    SectionControls,
    FlexBox,
    TraceLinkDisplay,
    TableChip,
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
          text: "Confidence Score",
          value: "score",
          groupable: false,
          divider: true,
        },
        {
          text: "Approval Status",
          value: "approvalStatus",
          filterable: true,
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
     * Determines whether to show approval for a link.
     *
     * @param link - The link to display.
     */
    showApproved(link: TraceLinkModel): boolean {
      return !this.approved.includes(link.traceLinkId);
    },
    /**
     * Determines whether to show decline for a link.
     *
     * @param link - The link to display.
     */
    showDeclined(link: TraceLinkModel): boolean {
      return !this.declined.includes(link.traceLinkId);
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
