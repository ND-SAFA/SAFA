<template>
  <details-panel panel="displayArtifactLevel" data-cy="panel-artifact-type">
    <artifact-level-buttons />
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
  ArtifactLevelButtons,
  ArtifactLevelContent,
  ArtifactLevelTraces,
  ArtifactLevelArtifacts,
} from "@/components/tim/display";
</script>
