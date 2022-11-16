<template>
  <div class="mt-4">
    <artifact-title />
    <artifact-traces />
    <artifact-documents />
    <artifact-errors />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import ArtifactTitle from "./ArtifactTitle.vue";
import ArtifactDocuments from "./ArtifactDocuments.vue";
import ArtifactErrors from "./ArtifactErrors.vue";
import ArtifactTraces from "./ArtifactTraces.vue";

/**
 * Displays artifact information.
 */
export default Vue.extend({
  name: "ArtifactContent",
  components: {
    ArtifactTitle,
    ArtifactDocuments,
    ArtifactErrors,
    ArtifactTraces,
  },
});
</script>
