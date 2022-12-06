<template>
  <table-header
    :headers="headers"
    :group-by.sync="currentGroup"
    :sort-by.sync="currentSort"
    :sort-desc.sync="currentSortDesc"
    :group-desc.sync="currentGroupDesc"
    :search-text.sync="currentSearch"
  >
    <template v-slot:right>
      <v-autocomplete
        outlined
        dense
        hide-details
        multiple
        label="Approval Types"
        v-model="currentApprovalTypes"
        :items="options"
        item-text="name"
        item-value="id"
        class="mb-1"
        data-cy="button-trace-link-generate-approval-type"
      />
    </template>
    <template v-slot:bottom>
      <v-btn text color="error" @click="handleClear">
        <v-icon class="mr-1">mdi-close-circle-multiple-outline</v-icon>
        Clear Unreviewed
      </v-btn>
    </template>
  </table-header>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DataTableHeader } from "vuetify";
import { approvalTypeOptions } from "@/util";
import { handleDeclineAll } from "@/api";
import { TableHeader } from "@/components/common";

/**
 * Displays the header for the trace links table.
 *
 * @emits-1 `update:searchText` (String) on search.
 * @emits-2 `update:sortBy` (String[]) on sort update.
 * @emits-3 `update:groupBy` (String) on group update.
 * @emits-3 `update:approvalTypes` (String) on approval type update.
 */
export default Vue.extend({
  name: "TraceApprovalTableHeader",
  components: {
    TableHeader,
  },
  props: {
    headers: {
      type: Array as PropType<DataTableHeader[]>,
      required: true,
    },
    searchText: String,
    groupBy: String,
    sortBy: Array as PropType<string[]>,
    groupDesc: Boolean,
    sortDesc: Boolean,
    approvalTypes: Array as PropType<string[]>,
  },
  data() {
    return {
      options: approvalTypeOptions(),
    };
  },
  computed: {
    /**
     * Emits changes to approval types.
     */
    currentApprovalTypes: {
      get(): string[] {
        return this.approvalTypes;
      },
      set(newTypes: string[]) {
        this.$emit("update:approvalTypes", newTypes);
      },
    },
    /**
     * Emits changes to the grouping.
     */
    currentSearch: {
      get(): string {
        return this.searchText;
      },
      set(newSearch: string): void {
        this.$emit("update:searchText", newSearch);
      },
    },
    /**
     * Emits changes to the sorting.
     */
    currentSort: {
      get(): string[] {
        return this.sortBy;
      },
      set(newSort: string[]): void {
        this.$emit("update:sortBy", newSort);
      },
    },
    /**
     * Emits changes to the grouping.
     */
    currentGroup: {
      get(): string {
        return this.groupBy;
      },
      set(newGroup: string): void {
        this.$emit("update:groupBy", newGroup);
      },
    },
    /**
     * Emits changes to the sorting order.
     */
    currentSortDesc: {
      get(): boolean {
        return this.sortDesc;
      },
      set(newDesc: boolean): void {
        this.$emit("update:sortDesc", newDesc);
      },
    },
    /**
     * Emits changes to the grouping order.
     */
    currentGroupDesc: {
      get(): boolean {
        return this.groupDesc;
      },
      set(newDesc: boolean): void {
        this.$emit("update:groupDesc", newDesc);
      },
    },
  },
  methods: {
    /**
     * Clears all unreviewed links.
     */
    handleClear(): void {
      handleDeclineAll();
    },
  },
});
</script>
