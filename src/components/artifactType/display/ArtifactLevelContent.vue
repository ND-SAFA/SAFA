<template>
  <panel-card borderless>
    <template #title>
      <typography
        ellipsis
        variant="subtitle"
        el="h1"
        :value="name"
        data-cy="text-selected-name"
      />
      <q-tooltip>{{ name }}</q-tooltip>
    </template>

    <template #title-actions>
      <icon :id="iconId" size="md" :color="iconColor" />
    </template>

    <typography variant="caption" value="Artifacts" />
    <typography el="p" :value="artifactCount" />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays attributes of the selected artifact level.
 */
export default {
  name: "ArtifactLevelContent",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { timStore } from "@/hooks";
import { PanelCard, Typography, Icon } from "@/components/common";

const artifactLevel = computed(() => timStore.selectedArtifactLevel);
const name = computed(() => artifactLevel.value?.name || "");
const artifactCount = computed(() => artifactLevel.value?.count || 0);

const iconId = computed(() => timStore.getTypeIcon(name.value));
const iconColor = computed(() => timStore.getTypeColor(name.value));
</script>
