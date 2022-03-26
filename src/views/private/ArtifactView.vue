<template>
  <private-page full-window>
    <template v-slot:page>
      <artifact-table />
      <artifact-tree />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
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
});
</script>
