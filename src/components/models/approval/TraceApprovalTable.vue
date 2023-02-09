<template>
  <panel-card>
    <typography el="h2" variant="subtitle" value="Approve Generated Links" />
    <typography
      el="p"
      b="4"
      value="Review, approve, and decline generated trace links."
    />
    <v-data-table
      v-model:sort-by="sortBy"
      v-model:group-by="groupBy"
      v-model:group-desc="groupDesc"
      v-model:sort-desc="sortDesc"
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
      item-key="traceLinkId"
      :items-per-page="50"
      data-cy="table-trace-link"
      @click:row="handleView($event)"
    >
      <template #top>
        <trace-approval-table-header
          v-model:group-by="groupBy"
          v-model:sort-by="sortBy"
          v-model:group-desc="groupDesc"
          v-model:sort-desc="sortDesc"
          v-model:search-text="searchText"
          v-model:approval-types="approvalTypes"
          :headers="headers"
        />
      </template>

      <template #[`group.header`]="data">
        <table-group-header
          show-expand
          :data="data"
          @open:all="handleOpenAll"
          @close:all="handleCloseAll"
        />
      </template>

      <template #[`item.sourceType`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip :value="item.sourceType" artifact-type />
        </td>
      </template>

      <template #[`item.targetType`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip :value="item.targetType" artifact-type />
        </td>
      </template>

      <template #[`item.approvalStatus`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip :value="item.approvalStatus" />
        </td>
      </template>

      <template #[`item.score`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip confidence-score :value="String(item.score)" />
        </td>
      </template>

      <template #[`item.actions`]="{ item }">
        <td class="v-data-table__divider" @click.stop="">
          <trace-link-approval :link="item" />
        </td>
      </template>

      <template #expanded-item="{ headers, item }">
        <td :colspan="headers.length" class="pb-2">
          <trace-link-display :link="item" :show-only="showOnly" />
        </td>
      </template>
    </v-data-table>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import {
  ApprovalType,
  FlatTraceLink,
  TraceTableGroup,
  DataTableHeader,
} from "@/types";
import { approvalStore, appStore, projectStore } from "@/hooks";
import { handleGetGeneratedLinks } from "@/api";
import {
  AttributeChip,
  TableGroupHeader,
  Typography,
  PanelCard,
} from "@/components/common";
import { TraceLinkDisplay, TraceLinkApproval } from "@/components/traceLink";
import traceApprovalTableHeaders from "./traceApprovalTableHeaders";
import TraceApprovalTableHeader from "./TraceApprovalTableHeader.vue";

/**
 * Displays a table of trace links.
 */
export default Vue.extend({
  name: "TraceApprovalTable",
  components: {
    PanelCard,
    TraceApprovalTableHeader,
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
      headers: traceApprovalTableHeaders,
      approvalTypes: [ApprovalType.UNREVIEWED],
    };
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
    visibleHeaders(): DataTableHeader<FlatTraceLink>[] {
      return this.headers.filter((header: DataTableHeader<FlatTraceLink>) => {
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
  mounted() {
    handleGetGeneratedLinks({});
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
