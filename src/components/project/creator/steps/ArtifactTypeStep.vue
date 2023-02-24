<template>
  <file-panel-list label="Artifact Type" variant="artifact" />
</template>

<script lang="ts">
/**
 * Provides inputs for uploading sets of artifacts.
 */
export default {
  name: "ArtifactTypeStep",
};
</script>

<script setup lang="ts">
import FilePanelList from "./FilePanelList.vue";
</script>
