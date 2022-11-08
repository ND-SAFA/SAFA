<template>
  <v-container>
    <typography
      el="p"
      b="4"
      value="Review, approve, and decline generated trace links."
    />
    <v-data-table
      class="trace-link-table"
      show-group-by
      show-expand
      single-expand
      multi-sort
      :headers="visibleHeaders"
      :items="visibleLinks"
      :expanded="selectedLinks"
      :search="searchText"
      :loading="isLoading"
      :sort-by.sync="sortBy"
      :group-by.sync="groupBy"
      :group-desc.sync="groupDesc"
      :sort-desc.sync="sortDesc"
      item-key="traceLinkId"
      :items-per-page="50"
      @click:row="handleView($event)"
    >
      <template v-slot:top>
        <trace-link-table-header
          :headers="headers"
          :group-by.sync="groupBy"
          :sort-by.sync="sortBy"
          :group-desc.sync="groupDesc"
          :sort-desc.sync="sortDesc"
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
          <trace-link-approval :link="item" />
        </td>
      </template>

      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length" class="pb-2">
          <trace-link-display :link="item" :show-only="showOnly" />
        </td>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { DataTableHeader } from "vuetify";
import { ApprovalType, FlatTraceLink, TraceTableGroup } from "@/types";
import { approvalStore, appStore, projectStore } from "@/hooks";
import { handleGetGeneratedLinks } from "@/api";
import {
  AttributeChip,
  TableGroupHeader,
  Typography,
} from "@/components/common";
import { TraceLinkDisplay, TraceLinkApproval } from "../base";
import traceLinkTableHeaders from "./traceLinkTableHeaders";
import TraceLinkTableHeader from "./TraceLinkTableHeader.vue";

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
    Typography,
  },
  data() {
    return {
      searchText: "",
      sortBy: ["score"] as (keyof FlatTraceLink)[],
      groupBy: "targetName" as keyof FlatTraceLink | undefined,
      sortDesc: true,
      groupDesc: false,
      headers: traceLinkTableHeaders,
      approvalTypes: [ApprovalType.UNREVIEWED],
    };
  },
  mounted() {
    handleGetGeneratedLinks({});
  },
  watch: {
    /**
     * Loads generated links when the route changes.
     */
    $route() {
      handleGetGeneratedLinks({});
    },
    /**
     * Loads generated links when the version changes.
     */
    versionId(newVersionId: string) {
      if (!newVersionId) return;

      handleGetGeneratedLinks({});
    },
  },
  computed: {
    /**
     * @return Whether the app is loading.
     */
    isLoading() {
      return appStore.isLoading > 0;
    },
    /**
     * @return The current project version.
     */
    versionId() {
      return projectStore.versionId;
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
      return approvalStore.traceLinks.filter(({ approvalStatus }) =>
        this.approvalTypes.includes(approvalStatus)
      );
    },
    /**
     * @return All selected links.
     */
    selectedLinks(): FlatTraceLink[] {
      return approvalStore.selectedLinks;
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
     * Opens all panels in the group.
     * @param data - The current grouping information.
     */
    handleOpenAll(data: TraceTableGroup) {
      approvalStore.selectLinks((link) => link[data.groupBy[0]] === data.group);
    },
    /**
     * Closes all panels in the group.
     * @param data - The current grouping information.
     */
    handleCloseAll(data: TraceTableGroup) {
      approvalStore.deselectLinks(
        (link) => link[data.groupBy[0]] !== data.group
      );
    },
    /**
     * Handles viewing a trace link.
     * @param link - The link to view.
     */
    handleView(link: FlatTraceLink) {
      approvalStore.toggleLink(link);
    },
  },
});
</script>
