<template>
  <v-container>
    <v-data-table
      class="trace-link-table"
      show-group-by
      show-expand
      single-expand
      multi-sort
      :headers="visibleHeaders"
      :items="visibleLinks"
      :expanded="expanded"
      :search="searchText"
      :loading="isLoading"
      :sort-by.sync="sortBy"
      :group-by.sync="groupBy"
      :sort-desc="true"
      item-key="traceLinkId"
      :items-per-page="50"
      @click:row="handleView($event)"
    >
      <template v-slot:top>
        <trace-link-table-header
          :headers="headers"
          :group-by.sync="groupBy"
          :sort-by.sync="sortBy"
          :search-text.sync="searchText"
          :approval-types.sync="approvalTypes"
        />
      </template>

      <template v-slot:[`group.header`]="data">
        <table-group-header
          show-expand
          :data="data"
          @open:all="handleOpenAll"
          @close:all="handleCloseAll"
        />
      </template>

      <template v-slot:[`item.sourceType`]="{ item }">
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

      <template v-slot:[`item.actions`]="{ item }">
        <td class="v-data-table__divider" @click.stop="">
          <trace-link-approval
            :link="item"
            @link:approve="handleApprove($event)"
            @link:decline="handleDecline($event)"
            @link:unreview="handleUnreview($event)"
          />
        </td>
      </template>

      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length" class="pb-2">
          <trace-link-display :link="item" hide-actions :show-only="showOnly" />
        </td>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { DataTableHeader } from "vuetify";
import {
  ApprovalType,
  FlatTraceLink,
  TraceTableGroup,
  VersionModel,
} from "@/types";
import { appModule, projectModule } from "@/store";
import { handleGetGeneratedLinks } from "@/api";
import { AttributeChip, TableGroupHeader } from "@/components/common";
import TraceLinkDisplay from "../TraceLinkDisplay.vue";
import TraceLinkApproval from "./TraceLinkApproval.vue";
import TraceLinkTableHeader from "./TraceLinkTableHeader.vue";
import traceLinkTableHeaders from "./traceLinkTableHeaders";

/**
 * Displays a table of trace links.
 */
export default Vue.extend({
  name: "TraceLinkTable",
  components: {
    TraceLinkTableHeader,
    TraceLinkApproval,
    TableGroupHeader,
    AttributeChip,
    TraceLinkDisplay,
  },
  data() {
    return {
      searchText: "",
      sortBy: ["score"] as (keyof FlatTraceLink)[],
      groupBy: "targetName" as keyof FlatTraceLink | undefined,
      headers: traceLinkTableHeaders,
      links: [] as FlatTraceLink[],
      expanded: [] as FlatTraceLink[],
      approved: [] as string[],
      declined: [] as string[],
      approvalTypes: [ApprovalType.UNREVIEWED],
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
    /**
     * @return What parts of the expansion panel to show.
     */
    showOnly(): undefined | "source" | "target" {
      if (this.groupBy?.includes("sourceName")) {
        return "target";
      } else if (this.groupBy?.includes("targetName")) {
        return "source";
      } else {
        return undefined;
      }
    },
    /**
     * @return All visible links.
     */
    visibleLinks(): FlatTraceLink[] {
      return this.links.filter(({ approvalStatus }) =>
        this.approvalTypes.includes(approvalStatus)
      );
    },
    /**
     * @return All visible links.
     */
    visibleHeaders(): Partial<DataTableHeader>[] {
      return this.headers.filter((header) => {
        return !(
          (this.approvalTypes.length === 1 &&
            header.value === "approvalStatus") ||
          (this.groupBy?.includes("sourceName") &&
            header.value === "sourceType") ||
          (this.groupBy?.includes("targetName") &&
            header.value === "targetType")
        );
      });
    },
  },
  methods: {
    /**
     * Loads the generated links for the current project.
     */
    async loadGeneratedLinks() {
      this.expanded = [];

      await handleGetGeneratedLinks({
        onSuccess: (generated) => {
          this.links = generated.links;
          this.approved = generated.approved;
          this.declined = generated.declined;
        },
        onError: () => {
          this.links = [];
          this.approved = [];
          this.declined = [];
        },
      });
    },
    /**
     * Opens all panels.
     */
    handleOpenAll(data: TraceTableGroup) {
      this.expanded = this.links.filter(
        (link) => link[data.groupBy[0]] === data.group
      );
    },
    /**
     * Closes all panels.
     */
    handleCloseAll(data: TraceTableGroup) {
      this.expanded = this.expanded.filter(
        (link) => link[data.groupBy[0]] !== data.group
      );
    },
    /**
     * Approves the given link and updates the stored links.
     *
     * @param link - The link to approve.
     */
    handleApprove(link: FlatTraceLink) {
      this.declined = this.declined.filter(
        (declinedId) => declinedId != link.traceLinkId
      );
      this.approved.push(link.traceLinkId);
      this.expanded = this.expanded.filter(
        (expandedLink) => expandedLink.traceLinkId !== link.traceLinkId
      );
    },
    /**
     * Declines the given link and updates the stored links.
     *
     * @param link - The link to decline.
     */
    handleDecline(link: FlatTraceLink) {
      this.approved = this.approved.filter(
        (declinedId) => declinedId != link.traceLinkId
      );
      this.declined.push(link.traceLinkId);
      this.expanded = this.expanded.filter(
        (expandedLink) => expandedLink.traceLinkId !== link.traceLinkId
      );
    },
    /**
     * Unreivews the given link and updates the stored links.
     *
     * @param link - The link to unreview.
     */
    handleUnreview(link: FlatTraceLink) {
      this.approved = this.approved.filter(
        (declinedId) => declinedId != link.traceLinkId
      );
      this.declined = this.declined.filter(
        (declinedId) => declinedId != link.traceLinkId
      );
      this.expanded = this.expanded.filter(
        (expandedLink) => expandedLink.traceLinkId !== link.traceLinkId
      );
    },
    /**
     * Handles viewing a trace link.
     *
     * @param link - The link to view.
     */
    handleView(link: FlatTraceLink) {
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
