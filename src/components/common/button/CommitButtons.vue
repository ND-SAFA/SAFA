<template>
  <flex-box>
    <template v-for="definition in buttons">
      <icon-button
        v-if="definition.handler"
        :key="definition.label"
        :color="props.color"
        :tooltip="definition.label"
        :icon="definition.icon"
        :disabled="definition.isDisabled"
        :data-cy="definition.dataCy"
        @click="definition.handler"
      />
    </template>
  </flex-box>
</template>

<script lang="ts">
/**
 * Renders buttons for undoing and redoing changes.
 */
export default {
  name: "CommitButtons",
};
</script>

<script setup lang="ts">
import { computed, withDefaults } from "vue";
import { ColorProps, IconVariant } from "@/types";
import { commitApiStore, commitStore } from "@/hooks";
import { FlexBox } from "@/components/common/display";
import IconButton from "./IconButton.vue";

const props = withDefaults(defineProps<ColorProps>(), {
  color: "primary",
});

const buttons = computed(() => [
  {
    handler: () => commitApiStore.handleUndo(),
    label: "Undo",
    icon: "undo" as IconVariant,
    isDisabled: !commitStore.canUndo,
    dataCy: "button-nav-undo",
  },
  {
    handler: () => commitApiStore.handleRedo(),
    label: "Redo",
    icon: "redo" as IconVariant,
    isDisabled: !commitStore.canRedo,
    dataCy: "button-nav-redo",
  },
]);
</script>
