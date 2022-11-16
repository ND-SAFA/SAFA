<template>
  <private-page full-window>
    <template v-slot:page>
      <artifact-table />
      <artifact-tree />
      <artifact-fab />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import {
  ArtifactTree,
  ArtifactTable,
  PrivatePage,
  ArtifactFab,
} from "@/components";

/**
 * Displays the artifact tree and table.
 */
export default Vue.extend({
  name: "ArtifactView",
  components: {
    ArtifactFab,
    ArtifactTable,
    PrivatePage,
    ArtifactTree,
  },
});
</script>
