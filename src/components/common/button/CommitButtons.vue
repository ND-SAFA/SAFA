<template>
  <flex-box>
    <icon-button
      tooltip="Undo changes"
      icon="undo"
      color="primary"
      :disabled="!commitStore.canUndo"
      data-cy="button-nav-undo"
      @click="commitApiStore.handleUndo"
    />
    <icon-button
      tooltip="Redo changes"
      icon="redo"
      color="primary"
      data-cy="button-nav-redo"
      :disabled="!commitStore.canRedo"
      @click="commitApiStore.handleRedo"
    />
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
import { commitApiStore, commitStore } from "@/hooks";
import { FlexBox } from "@/components/common/display";
import IconButton from "./IconButton.vue";
</script>
