<template>
  <table-header
    :headers="headers"
    :search-text.sync="currentSearch"
    :group-by.sync="currentGroup"
    :sort-by.sync="currentSort"
    :sort-desc.sync="currentSortDesc"
    :group-desc.sync="currentGroupDesc"
    data-cy="table-header"
  >
    <template v-slot:right>
      <flex-box>
        <v-divider vertical />
        <v-autocomplete
          outlined
          multiple
          dense
          hide-details
          label="Row Types"
          v-model="currentRowTypes"
          :items="artifactTypes"
          style="max-width: 300px"
          class="mx-2"
          data-cy="input-trace-matrix-table-row-types"
        />
        <v-autocomplete
          outlined
          multiple
          dense
          hide-details
          label="Column Types"
          v-model="currentColTypes"
          :items="artifactTypes"
          style="max-width: 300px"
          data-cy="input-trace-matrix-table-col-types"
        />
      </flex-box>
    </template>
  </table-header>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DataTableHeader } from "vuetify";
import { typeOptionsStore } from "@/hooks";
import { TableHeader, FlexBox } from "@/components/common";

/**
 * Represents the header and inputs for a table of trace links.
 *
 * @emits-1 `update:searchText` (String) on search.
 * @emits-2 `update:sortBy` (String[]) on sort update.
 * @emits-3 `update:groupBy` (String) on group update.
 * @emits-3 `update:rowTypes` (String[]) on row filter update.
 * @emits-3 `update:colTypes` (String[]) on column filter update.
 */
export default Vue.extend({
  name: "TraceMatrixTableHeader",
  components: {
    FlexBox,
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
    rowTypes: Array as PropType<string[]>,
    colTypes: Array as PropType<string[]>,
  },
  computed: {
    /**
     * @return All types of artifacts in the current project.
     */
    artifactTypes(): string[] {
      return typeOptionsStore.artifactTypes;
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
    /**
     * Emits changes to the column types.
     */
    currentRowTypes: {
      get(): string[] {
        return this.rowTypes;
      },
      set(newTypes: string[]): void {
        this.$emit("update:rowTypes", newTypes);
      },
    },
    /**
     * Emits changes to the row types.
     */
    currentColTypes: {
      get(): string[] {
        return this.colTypes;
      },
      set(newTypes: string[]): void {
        this.$emit("update:colTypes", newTypes);
      },
    },
  },
});
</script>
