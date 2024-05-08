<template>
  <details-panel panel="displayArtifact">
    <template #actions>
      <artifact-buttons />
    </template>
    <artifact-content />
    <artifact-context v-if="ENABLED_FEATURES.NASA_ARTIFACT_RELATIONS" />
    <artifact-traces v-else />
    <artifact-comments />
    <artifact-health />
    <artifact-documents />
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
  ArtifactContext,
} from "@/components/artifact/display";
import {
  ArtifactButtons,
  ArtifactComments,
  ArtifactHealth,
} from "@/components/artifact/save";
</script>
