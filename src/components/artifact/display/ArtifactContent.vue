<template>
  <div>
    <artifact-fields />
    <artifact-traces />
    <artifact-documents />
    <artifact-errors />
  </div>
</template>

<script lang="ts">
/**
 * Displays artifact information.
 */
export default {
  name: "ArtifactContent",
};
</script>

<script setup lang="ts">
import ArtifactFields from "./ArtifactFields.vue";
import ArtifactDocuments from "./ArtifactDocuments.vue";
import ArtifactErrors from "./ArtifactErrors.vue";
import ArtifactTraces from "./ArtifactTraces.vue";
</script>
