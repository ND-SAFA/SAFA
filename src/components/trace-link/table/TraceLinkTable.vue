<template>
  <v-container>
    <v-data-table
      class="trace-link-table"
      show-group-by
      show-expand
      single-expand
      multi-sort
      :headers="headers"
      :items="links"
      :expanded="expanded"
      :search="searchText"
      :loading="isLoading"
      :sort-by.sync="sortBy"
      :group-by.sync="groupBy"
      :group-desc="true"
      item-key="traceLinkId"
      :items-per-page="50"
      @click:row="handleView($event)"
    >
      <template v-slot:top>
        <table-header
          :headers="headers"
          :group-by.sync="groupBy"
          :sort-by.sync="sortBy"
          :search-text.sync="searchText"
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
import { FlatTraceLink, TraceTableGroup, VersionModel } from "@/types";
import { appModule, projectModule } from "@/store";
import { handleGetGeneratedLinks } from "@/api";
import {
  AttributeChip,
  TableGroupHeader,
  TableHeader,
} from "@/components/common";
import TraceLinkDisplay from "../TraceLinkDisplay.vue";
import TraceLinkApproval from "./TraceLinkApproval.vue";

/**
 * Displays a table of trace links.
 */
export default Vue.extend({
  name: "TraceLinkTable",
  components: {
    TraceLinkApproval,
    TableHeader,
    TableGroupHeader,
    AttributeChip,
    TraceLinkDisplay,
  },
  data() {
    return {
      searchText: "",
      sortBy: ["targetName", "sourceName"] as (keyof FlatTraceLink)[],
      groupBy: "approvalStatus" as keyof FlatTraceLink,
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
          text: "Actions",
          value: "actions",
          groupable: false,
          divider: true,
        },
        {
          value: "data-table-expand",
          groupable: false,
        },
      ],
      links: [] as FlatTraceLink[],
      expanded: [] as FlatTraceLink[],
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
    /**
     * @return What parts of the expansion panel to show.
     */
    showOnly(): undefined | "source" | "target" {
      if (this.groupBy.includes("sourceName")) {
        return "target";
      } else if (this.groupBy.includes("targetName")) {
        return "source";
      } else {
        return undefined;
      }
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
