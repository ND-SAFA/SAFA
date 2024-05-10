<template>
  <details-panel panel="saveArtifact" data-cy="panel-artifact-save">
    <template #actions>
      <text-button
        text
        label="View Artifact"
        icon="artifact"
        @click="appStore.openDetailsPanel('displayArtifact')"
      />
    </template>
    <panel-card title="Save Artifact" borderless>
      <save-artifact-inputs />
      <template #actions>
        <save-artifact-buttons />
      </template>
    </panel-card>
    <artifact-health v-if="permissionStore.isNASA" />
  </details-panel>
</template>

<script lang="ts">
/**
 * Allows for creating and editing artifacts.
 */
export default {
  name: "SaveArtifactPanel",
};
</script>

<script setup lang="ts">
import { appStore, permissionStore } from "@/hooks";
import { DetailsPanel, PanelCard, TextButton } from "@/components/common";
import {
  SaveArtifactInputs,
  SaveArtifactButtons,
  ArtifactHealth,
} from "@/components/artifact/save";
</script>
