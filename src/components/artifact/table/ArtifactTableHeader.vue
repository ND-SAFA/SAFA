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
    <template slot="right">
      <v-autocomplete
        outlined
        multiple
        dense
        hide-details
        v-if="inDeltaView"
        label="Delta Types"
        v-model="selectedDeltaTypes"
        :items="deltaTypes"
        item-text="name"
        item-value="id"
        style="width: 200px"
        class="mb-1"
      />
    </template>
  </table-header>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DataTableHeader } from "vuetify";
import { ArtifactDeltaState } from "@/types";
import { deltaTypeOptions } from "@/util";
import { deltaStore } from "@/hooks";
import { TableHeader } from "@/components/common";

/**
 * Represents the header and inputs for a table of artifacts.
 *
 * @emits-1 `update:searchText` (String) on search.
 * @emits-2 `update:sortBy` (String[]) on sort update.
 * @emits-3 `update:groupBy` (String) on group update.
 * @emits-4 `filter` (ArtifactDeltaState[]) - On filter search.
 */
export default Vue.extend({
  name: "ArtifactTableHeader",
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
  },
  data() {
    return {
      selectedDeltaTypes: [] as ArtifactDeltaState[],
      deltaTypes: deltaTypeOptions(),
    };
  },
  computed: {
    /**
     * @return Whether the app is in delta view.
     */
    inDeltaView(): boolean {
      return deltaStore.inDeltaView;
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
  watch: {
    /**
     * Emits the selected delta types on change.
     */
    selectedDeltaTypes(items: ArtifactDeltaState[]) {
      this.$emit("filter", items);
    },
  },
});
</script>

<style scoped></style>
