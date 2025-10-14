<template>
  <type-buttons
    v-if="layoutStore.isTreeMode"
    :default-visible="!smallWindow"
    :hidden-types="hiddenTypes"
    class="q-mb-sm q-mr-xs"
    @click="handleClick"
  />
</template>

<script lang="ts">
/**
 * Buttons for changing which artifact types are visible.
 */
export default {
  name: "VisibleTypeButtons",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactTypeSchema } from "@/types";
import { layoutStore, selectionStore, useScreen } from "@/hooks";
import { TypeButtons } from "@/components/common";

const { smallWindow } = useScreen();

const hiddenTypes = computed(() => selectionStore.ignoreTypes);

/**
 * Toggles whether a type is visible.
 * @param option - The type to toggle.
 */
function handleClick(option: ArtifactTypeSchema) {
  const hidden = hiddenTypes.value.find((type) => type === option.name);

  selectionStore.filterGraph({
    type: "ignore",
    ignoreType: option.name,
    action: hidden ? "remove" : "add",
  });
}
</script>
