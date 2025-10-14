<template>
  <details-panel panel="displayArtifactBody">
    <template #actions>
      <text-button
        text
        label="Artifact"
        icon="artifact"
        @click="appStore.openDetailsPanel('displayArtifact')"
      />
    </template>
    <artifact-body />
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays artifact content.
 */
export default {
  name: "ArtifactBodyPanel",
};
</script>

<script setup lang="ts">
import { appStore } from "@/hooks";
import { DetailsPanel, TextButton } from "@/components/common";
import { ArtifactBody } from "@/components/artifact/display";
</script>
