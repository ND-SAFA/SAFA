<template>
  <panel-card v-if="inDeltaView" title="Artifacts" collapsable borderless>
    <delta-button-group
      delta-type="added"
      :items="addedArtifacts"
      @click="handleAddedSelect"
    />
    <delta-button-group
      delta-type="modified"
      :items="modifiedArtifacts"
      @click="handleModifiedSelect"
    />
    <delta-button-group
      delta-type="removed"
      :items="removedArtifacts"
      @click="handleRemovedSelect"
    />

    <artifact-delta-diff
      v-if="!!selectedDelta"
      :open="!!selectedDelta"
      :delta="selectedDelta"
      @close="selectedDelta = undefined"
    />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays artifact delta information.
 */
export default {
  name: "ArtifactDeltas",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { DeltaType, ArtifactDeltaSchema, ChangedArtifact } from "@/types";
import { deltaStore } from "@/hooks";
import { PanelCard } from "@/components/common";
import ArtifactDeltaDiff from "./ArtifactDeltaDiff.vue";
import DeltaButtonGroup from "./DeltaButtonGroup.vue";

const selectedDelta = ref<ChangedArtifact | undefined>();

const inDeltaView = computed(() => deltaStore.inDeltaView);
const addedArtifacts = computed(() => deltaStore.addedArtifacts);
const modifiedArtifacts = computed(() => deltaStore.modifiedArtifacts);
const removedArtifacts = computed(() => deltaStore.removedArtifacts);

/**
 * Selects an artifact.
 */
function handleArtifactSelect(
  name: string,
  artifact: ArtifactDeltaSchema,
  deltaType: DeltaType
): void {
  selectedDelta.value = { name, artifact, deltaType };
}

/**
 * Selects an added artifact.
 * @param id - The artifact to select.
 */
function handleAddedSelect(id: string): void {
  handleArtifactSelect(
    addedArtifacts.value[id].name,
    addedArtifacts.value[id],
    "added"
  );
}

/**
 * Selects a modified artifact.
 * @param id - The artifact to select.
 */
function handleModifiedSelect(id: string): void {
  handleArtifactSelect(
    modifiedArtifacts.value[id].after.name,
    modifiedArtifacts.value[id],
    "modified"
  );
}

/**
 * Selects a removed artifact.
 * @param id - The artifact to select.
 */
function handleRemovedSelect(id: string): void {
  handleArtifactSelect(
    removedArtifacts.value[id].name,
    removedArtifacts.value[id],
    "removed"
  );
}
</script>
