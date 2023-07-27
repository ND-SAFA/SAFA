<template>
  <div />
</template>

<script lang="ts">
/**
 * A wrapper for managing a right click context menu on the graph.
 */
export default {
  name: "CyContextMenu",
};
</script>

<script setup lang="ts">
import { inject } from "vue";
import { Core } from "cytoscape";

const cy = inject<Promise<Core>>("cy");
</script>
