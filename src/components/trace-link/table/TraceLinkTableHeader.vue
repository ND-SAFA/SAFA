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
    <section-controls @open:all="handleOpenAll" @close:all="handleCloseAll" />
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { FlexBox } from "@/components/common";
import SectionControls from "./SectionControls.vue";

/**
 * Renders the header to the trace link table.
 *
 * @emits-1 `search` (String) on search.
 * @emits-2 `open:all` on expand all items.
 * @emits-2 `close:all` on collapse all items.
 */
export default Vue.extend({
  name: "TraceLinkTableHeader",
  components: { FlexBox, SectionControls },
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
  methods: {
    /**
     * Emits a call to open all items.
     */
    handleOpenAll() {
      this.$emit("open:all");
    },
    /**
     * Emits a call to close all items.
     */
    handleCloseAll() {
      this.$emit("close:all");
    },
  },
});
</script>

<style scoped></style>
