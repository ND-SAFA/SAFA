<template>
  <details-panel panel="displayArtifactLevel" data-cy="panel-artifact-type">
    <template #actions>
      <artifact-level-buttons />
    </template>
    <artifact-level-content />
    <artifact-level-traces />
    <artifact-level-artifacts />
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays artifact level information.
 */
export default {
  name: "ArtifactLevelPanel",
};
</script>

<script setup lang="ts">
import { DetailsPanel } from "@/components/common";
import {
  ArtifactLevelContent,
  ArtifactLevelTraces,
  ArtifactLevelArtifacts,
} from "@/components/artifactType/display";
import { ArtifactLevelButtons } from "@/components/artifactType/save";
</script>
