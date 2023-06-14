<template>
  <q-card
    :bordered="visible"
    flat
    :class="visible ? 'bd-primary q-mx-sm' : 'q-mx-sm'"
  >
    <q-btn-group flat>
      <icon-button
        v-for="level of artifactLevels"
        v-show="visible"
        :key="level.typeId"
        v-bind="buttonProps(level)"
        dense
        :tooltip-delay="0"
        data-cy="button-nav-type"
        icon="artifact"
        @click="handleClick(level)"
      />
      <separator v-show="visible" vertical color="primary" />
      <icon-button
        dense
        tooltip="Filter Types"
        color="primary"
        :icon="visible ? 'filter-close' : 'filter-open'"
        @click="visible = !visible"
      />
    </q-btn-group>
  </q-card>
</template>

<script lang="ts">
/**
 * Buttons for changing which artifact types are visible.
 */
export default {
  name: "TypeButtons",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { TimArtifactLevelSchema } from "@/types";
import { selectionStore, typeOptionsStore } from "@/hooks";
import { IconButton } from "@/components/common";
import Separator from "@/components/common/display/content/Separator.vue";

const visible = ref(false);

const hiddenTypes = computed(() => selectionStore.ignoreTypes);
const artifactLevels = computed(() => typeOptionsStore.artifactLevels);

/**
 * Returns props for a type button.
 * @param option - The type button to get props for.
 */
function buttonProps(option: TimArtifactLevelSchema) {
  const hidden = hiddenTypes.value.find((type) => type === option.name);

  return {
    style: `color: ${option.color};` + (hidden ? "opacity: 0.3" : ""),
    tooltip: option.name,
    class: !hidden ? "nav-mode-selected" : "",
  };
}

/**
 * Toggles whether a type is visible.
 * @param option - The type to toggle.
 */
function handleClick(option: TimArtifactLevelSchema) {
  const hidden = hiddenTypes.value.find((type) => type === option.name);

  selectionStore.filterGraph({
    type: "ignore",
    ignoreType: option.name,
    action: hidden ? "remove" : "add",
  });
}
</script>
