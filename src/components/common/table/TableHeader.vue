<template>
  <v-row dense class="mb-2">
    <v-col cols="12">
      <flex-box align="center">
        <v-text-field
          dense
          outlined
          clearable
          hide-details
          label="Search"
          style="width: 100%"
          v-model="currentSearch"
          append-icon="mdi-magnify"
        />
        <commit-buttons v-if="showCommitButtons" color="primary" class="mx-2" />
      </flex-box>
    </v-col>
    <v-col cols="12">
      <flex-box>
        <v-autocomplete
          clearable
          outlined
          dense
          hide-details
          label="Group By"
          v-model="currentGroup"
          :items="options"
          item-text="text"
          item-value="value"
          :prepend-inner-icon="`mdi-arrow-${
            currentGroupDesc ? 'up' : 'down'
          }-thin-circle-outline`"
          @click:prepend-inner="currentGroupDesc = !currentGroupDesc"
          data-cy="artifact-table-group-by"
          style="max-width: 300px"
        />
        <v-autocomplete
          outlined
          multiple
          dense
          hide-details
          label="Sort By"
          v-model="currentSort"
          :items="options"
          item-text="text"
          item-value="value"
          class="mx-2"
          :prepend-inner-icon="`mdi-arrow-${
            currentSortDesc ? 'up' : 'down'
          }-thin-circle-outline`"
          @click:prepend-inner="currentSortDesc = !currentSortDesc"
          data-cy="artifact-table-sort-by"
          style="max-width: 300px"
        />
        <slot name="right" />
      </flex-box>
    </v-col>
    <v-col cols="12">
      <slot name="bottom" />
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DataTableHeader } from "vuetify";
import { FlexBox } from "@/components/common/layout";
import { CommitButtons } from "@/components/common/button";
/**
 * Renders the header for a table.
 *
 * @emits-1 `update:searchText` (String) on search.
 * @emits-2 `update:sortBy` (String[]) on sort update.
 * @emits-3 `update:groupBy` (String) on group update.
 */
export default Vue.extend({
  name: "TableHeader",
  components: { FlexBox, CommitButtons },
  props: {
    headers: {
      type: Array as PropType<DataTableHeader[]>,
      required: true,
    },
    searchText: String,
    groupBy: String,
    groupDesc: Boolean,
    sortBy: Array as PropType<string[]>,
    sortDesc: Boolean,
    showCommitButtons: Boolean,
  },
  computed: {
    options() {
      return this.headers
        .filter(({ text }) => !!text && text !== "Actions")
        .map(({ text, value }) => ({ text, value }));
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
     * Emits the current search text on change.
     */
    searchText(search: string) {
      this.$emit("search", search);
    },
  },
});
</script>

<style scoped></style>
