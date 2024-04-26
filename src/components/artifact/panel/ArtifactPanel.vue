<template>
  <details-panel panel="displayArtifact">
    <template #actions>
      <artifact-buttons />
    </template>
    <artifact-content />
    <artifact-comments />
    <artifact-context v-if="ENABLED_FEATURES.NASA_ARTIFACT_RELATIONS" />
    <artifact-traces v-else />
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
import { ENABLED_FEATURES } from "@/util";
import { DetailsPanel } from "@/components/common";
import {
  ArtifactContent,
  ArtifactDocuments,
  ArtifactTraces,
  ArtifactErrors,
  ArtifactContext,
} from "@/components/artifact/display";
import { ArtifactButtons, ArtifactComments } from "@/components/artifact/save";
</script>
