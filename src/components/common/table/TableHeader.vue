<template>
  <flex-box justify="space-between" b="2">
    <div>
      <v-text-field
        dense
        outlined
        clearable
        hide-details
        label="Search"
        style="width: 30vw"
        v-model="currentSearch"
        append-icon="mdi-magnify"
      />
      <flex-box align="center">
        <commit-buttons color="primary" class="mt-2" />
        <slot name="bottom" />
      </flex-box>
    </div>
    <div>
      <slot name="right" />
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
          style="max-width: 200px"
          :prepend-inner-icon="`mdi-arrow-${
            currentGroupDesc ? 'up' : 'down'
          }-thin-circle-outline`"
          @click:prepend-inner="currentGroupDesc = !currentGroupDesc"
          data-cy="artifact-table-group-by"
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
          style="max-width: 200px"
          class="ml-1"
          :prepend-inner-icon="`mdi-arrow-${
            currentSortDesc ? 'up' : 'down'
          }-thin-circle-outline`"
          @click:prepend-inner="currentSortDesc = !currentSortDesc"
          data-cy="artifact-table-sort-by"
        />
      </flex-box>
    </div>
  </flex-box>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DataTableHeader } from "vuetify";
import { FlexBox } from "@/components/common";
import CommitButtons from "@/components/navigation/header/CommitButtons.vue";
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
