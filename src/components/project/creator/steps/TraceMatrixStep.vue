<template>
  <file-panel-list label="Trace Matrix" variant="trace" />
</template>

<script lang="ts">
/**
 * Provides inputs for uploading matrices of trace links.
 */
export default {
  name: "TraceMatrixStep",
};
</script>

<script setup lang="ts">
import FilePanelList from "./FilePanelList.vue";
</script>
