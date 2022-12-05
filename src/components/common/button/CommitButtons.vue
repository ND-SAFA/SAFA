<template>
  <flex-box>
    <template v-for="definition in changeButtons">
      <generic-icon-button
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
import Vue from "vue";
import { ButtonDefinition, ButtonType } from "@/types";
import { commitStore } from "@/hooks";
import { redoCommit, undoCommit } from "@/api";
import { FlexBox } from "@/components/common/layout";
import GenericIconButton from "./GenericIconButton.vue";

export default Vue.extend({
  name: "CommitButtons",
  components: {
    FlexBox,
    GenericIconButton,
  },
  props: {
    color: {
      type: String,
      default: "accent",
    },
  },
  computed: {
    /**
     * @return The change buttons.
     */
    changeButtons(): ButtonDefinition[] {
      return [
        {
          type: ButtonType.ICON,
          handler: () => {
            undoCommit().then();
          },
          label: "Undo",
          icon: "mdi-undo",
          isDisabled: !commitStore.canUndo,
        },
        {
          type: ButtonType.ICON,
          handler: () => redoCommit().then(),
          label: "Redo",
          icon: "mdi-redo",
          isDisabled: !commitStore.canRedo,
        },
      ];
    },
  },
});
</script>
