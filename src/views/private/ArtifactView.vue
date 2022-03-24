<template>
  <private-page full-window>
    <template v-slot:page>
      <artifact-tree v-if="!isTableView" />
      <artifact-table v-if="isTableView" />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { documentModule } from "@/store";
import { ArtifactTree, ArtifactTable, PrivatePage } from "@/components";

/**
 * Displays the artifact tree of the current project with a label
 * above it containing the current project and version.
 */
export default Vue.extend({
  name: "artifact-view",
  components: {
    ArtifactTable,
    PrivatePage,
    ArtifactTree,
  },
  computed: {
    isTableView(): boolean {
      return documentModule.isTableDocument;
    },
  },
});
</script>
