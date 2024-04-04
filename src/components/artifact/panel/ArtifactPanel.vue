<template>
  <details-panel panel="displayArtifact">
    <template #actions>
      <artifact-buttons />
    </template>
    <artifact-content />
    <artifact-traces />
    <artifact-documents />
    <artifact-errors />
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays artifact information.
 */
export default {
  name: "ArtifactPanel",
};
</script>

<script setup lang="ts">
import { DetailsPanel } from "@/components/common";
import {
  ArtifactContent,
  ArtifactDocuments,
  ArtifactTraces,
  ArtifactErrors,
} from "@/components/artifact/display";
import { ArtifactButtons } from "@/components/artifact/save";
</script>
