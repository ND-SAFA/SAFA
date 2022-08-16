<template>
  <flex-box justify="space-between" b="2">
    <v-text-field
      dense
      outlined
      clearable
      label="Search Trace Links"
      style="max-width: 30vw"
      v-model="currentSearch"
      append-icon="mdi-magnify"
    />
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
        />
      </flex-box>
    </div>
  </flex-box>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { FlexBox } from "@/components/common";
import { DataTableHeader } from "vuetify";
/**
 * Renders the header for a table.
 *
 * @emits-1 `update:searchText` (String) on search.
 * @emits-2 `update:sortBy` (String[]) on sort update.
 * @emits-3 `update:groupBy` (String) on group update.
 */
export default Vue.extend({
  name: "TableHeader",
  components: { FlexBox },
  props: {
    headers: {
      type: Array as PropType<DataTableHeader[]>,
      required: true,
    },
    searchText: String,
    groupBy: String,
    sortBy: Array as PropType<string[]>,
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
