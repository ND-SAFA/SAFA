<template>
  <details-panel panel="saveArtifactLevel" data-cy="panel-save-artifact-type">
    <flex-box b="2">
      <text-button
        text
        label="View Type"
        icon="artifact"
        @click="appStore.openDetailsPanel('displayArtifactLevel')"
      />
    </flex-box>

    <panel-card
      v-if="artifactLevel"
      :title="artifactLevel.name"
      data-cy="panel-artifact-type-options"
    >
      <type-direction-input :artifact-type="artifactLevel" />
      <type-icon-input :artifact-type="artifactLevel" />
      <type-color-input :artifact-type="artifactLevel" />
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
/**
 * Allows for editing the artifact level information.
 */
export default {
  name: "SaveArtifactLevelPanel",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore, selectionStore } from "@/hooks";
import {
  PanelCard,
  TypeDirectionInput,
  TypeIconInput,
  DetailsPanel,
  FlexBox,
  TextButton,
} from "@/components/common";
import TypeColorInput from "@/components/common/input/TypeColorInput.vue";

const artifactLevel = computed(() => selectionStore.selectedArtifactLevel);
</script>
