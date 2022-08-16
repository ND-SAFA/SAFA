<template>
  <flex-box justify="space-between">
    <v-text-field
      dense
      outlined
      clearable
      label="Search Trace Links"
      style="max-width: 600px"
      v-model="searchText"
      append-icon="mdi-magnify"
    />
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
        style="width: 200px"
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
        style="width: 200px"
        class="ml-1"
      />
    </flex-box>
  </flex-box>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { FlexBox } from "@/components/common";
import { DataTableHeader } from "vuetify";
import { FlatTraceLink } from "@/types";

/**
 * Renders the header to the trace link table.
 *
 * @emits-1 `search` (String) on search.
 */
export default Vue.extend({
  name: "TraceLinkTableHeader",
  components: { FlexBox },
  props: {
    headers: {
      type: Array as PropType<DataTableHeader[]>,
      required: true,
    },
    groupBy: String as PropType<keyof FlatTraceLink>,
    sortBy: Array as PropType<(keyof FlatTraceLink)[]>,
  },
  data() {
    return {
      searchText: "",
    };
  },
  computed: {
    options() {
      return this.headers
        .filter(({ text }) => !!text)
        .map(({ text, value }) => ({ text, value }));
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
