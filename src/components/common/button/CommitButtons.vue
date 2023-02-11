<template>
  <flex-box>
    <template v-for="definition in buttons">
      <icon-button
        v-if="definition.handler"
        :key="definition.label"
        :color="color"
        :tooltip="definition.label"
        :icon-id="definition.icon"
        :is-disabled="definition.isDisabled"
        :data-cy="definition.dataCy"
        @click="definition.handler"
      />
    </template>
  </flex-box>
</template>

<script lang="ts">
export default {
  name: "CommitButtons",
};
</script>

<script setup lang="ts">
import { computed, withDefaults, defineProps } from "vue";
import { ButtonType } from "@/types";
import { commitStore } from "@/hooks";
import { redoCommit, undoCommit } from "@/api";
import { FlexBox } from "@/components/common/layout";
import IconButton from "./IconButton.vue";

const props = withDefaults(
  defineProps<{
    color?: string;
  }>(),
  {
    color: "accent",
  }
);

const buttons = computed(() => [
  {
    type: ButtonType.ICON,
    handler: () => {
      undoCommit().then();
    },
    label: "Undo",
    icon: "mdi-undo",
    isDisabled: !commitStore.canUndo,
    dataCy: "button-nav-undo",
  },
  {
    type: ButtonType.ICON,
    handler: () => redoCommit().then(),
    label: "Redo",
    icon: "mdi-redo",
    isDisabled: !commitStore.canRedo,
    dataCy: "button-nav-redo",
  },
]);
</script>
