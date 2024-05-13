<template>
  <details-panel panel="displayArtifact">
    <template #actions>
      <artifact-buttons />
    </template>
    <artifact-content />
    <artifact-context v-if="permissionStore.isNASA" />
    <artifact-traces v-else />
    <artifact-comments />
    <artifact-health />
    <artifact-views />
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
import { permissionStore } from "@/hooks";
import { DetailsPanel } from "@/components/common";
import {
  ArtifactContent,
  ArtifactViews,
  ArtifactTraces,
  ArtifactContext,
} from "@/components/artifact/display";
import {
  ArtifactButtons,
  ArtifactComments,
  ArtifactHealth,
} from "@/components/artifact/save";
</script>
