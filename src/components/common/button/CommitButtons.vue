<template>
  <flex-box>
    <template v-for="definition in buttons">
      <icon-button
        v-if="definition.handler"
        :key="definition.label"
        :color="color"
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
import { ThemeColor } from "@/types";
import { commitStore } from "@/hooks";
import { redoCommit, undoCommit } from "@/api";
import { FlexBox } from "@/components/common/layout";
import IconButton from "./IconButton.vue";

withDefaults(
  defineProps<{
    /**
     * The color to render the component with.
     */
    color?: ThemeColor;
  }>(),
  {
    color: "accent",
  }
);

const buttons = computed(() => [
  {
    handler: () => {
      undoCommit().then();
    },
    label: "Undo",
    icon: "undo",
    isDisabled: !commitStore.canUndo,
    dataCy: "button-nav-undo",
  },
  {
    handler: () => redoCommit().then(),
    label: "Redo",
    icon: "redo",
    isDisabled: !commitStore.canRedo,
    dataCy: "button-nav-redo",
  },
]);
</script>
