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
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { FlexBox } from "@/components/common";

/**
 * Renders the header to the trace link table.
 *
 * @emits-1 `search` (String) on search.
 */
export default Vue.extend({
  name: "TraceLinkTableHeader",
  components: { FlexBox },
  data() {
    return {
      searchText: "",
    };
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
