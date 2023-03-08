<template>
  <panel-card v-if="doDisplay" title="Warnings" data-cy="artifact-warnings">
    <template #title-actions>
      <icon variant="warning" />
    </template>

    <toggle-list
      v-for="(warning, idx) in warnings"
      :key="idx"
      :title="warning.ruleName"
    >
      <typography :value="warning.ruleMessage" />
    </toggle-list>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the selected node's error.
 */
export default {
  name: "ArtifactErrors",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { selectionStore, warningStore } from "@/hooks";
import { Typography, ToggleList, PanelCard, Icon } from "@/components/common";

const artifact = computed(() => selectionStore.selectedArtifact);

const warnings = computed(() => {
  const id = artifact.value?.id || "";

  return warningStore.artifactWarnings[id] || [];
});

const doDisplay = computed(() => warnings.value.length > 0);
</script>
