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
import {
  ArtifactTitle,
  ArtifactDocuments,
  ArtifactErrors,
  ArtifactTraces,
} from "./content";

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
