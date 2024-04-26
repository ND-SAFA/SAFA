<template>
  <details-panel panel="saveArtifactLevel" data-cy="panel-save-artifact-type">
    <template #actions>
      <text-button
        text
        label="View Type"
        icon="artifact"
        @click="appStore.openDetailsPanel('displayArtifactLevel')"
      />
    </template>

    <panel-card
      v-if="artifactLevel"
      data-cy="panel-artifact-type-options"
      borderless
    >
      <flex-box align="center" justify="between">
        <typography
          ellipsis
          variant="subtitle"
          el="h1"
          :value="name"
          data-cy="text-selected-name"
        />
        <q-tooltip>{{ name }}</q-tooltip>
        <icon :id="iconId" size="md" :color="iconColor" />
      </flex-box>

      <separator b="2" />
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
import { appStore, timStore } from "@/hooks";
import {
  PanelCard,
  TypeDirectionInput,
  TypeIconInput,
  DetailsPanel,
  FlexBox,
  TextButton,
  Icon,
  Separator,
  Typography,
  TypeColorInput,
} from "@/components/common";

const artifactLevel = computed(() => timStore.selectedArtifactLevel);
const name = computed(() => artifactLevel.value?.name || "");
const iconId = computed(() => timStore.getTypeIcon(name.value));
const iconColor = computed(() => timStore.getTypeColor(name.value));
</script>
