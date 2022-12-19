<template>
  <div class="py-4">
    <artifact-fields />
    <artifact-traces />
    <artifact-documents />
    <artifact-errors />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import ArtifactFields from "./ArtifactFields.vue";
import ArtifactDocuments from "./ArtifactDocuments.vue";
import ArtifactErrors from "./ArtifactErrors.vue";
import ArtifactTraces from "./ArtifactTraces.vue";

/**
 * Displays artifact information.
 */
export default Vue.extend({
  name: "ArtifactContent",
  components: {
    ArtifactFields,
    ArtifactDocuments,
    ArtifactErrors,
    ArtifactTraces,
  },
});
</script>
