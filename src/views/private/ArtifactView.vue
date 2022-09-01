<template>
  <private-page full-window>
    <template v-slot:page>
      <artifact-table />
      <artifact-tree />
      <artifact-fab />

      <artifact-creator-modal />
      <trace-link-creator-modal />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import {
  ArtifactTree,
  ArtifactTable,
  PrivatePage,
  ArtifactCreatorModal,
  ArtifactFab,
  TraceLinkCreatorModal,
} from "@/components";

/**
 * Displays the artifact tree and table.
 */
export default Vue.extend({
  name: "ArtifactView",
  components: {
    TraceLinkCreatorModal,
    ArtifactFab,
    ArtifactTable,
    PrivatePage,
    ArtifactTree,
    ArtifactCreatorModal,
  },
});
</script>
