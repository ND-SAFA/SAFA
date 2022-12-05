<template>
  <flex-box>
    <generic-icon-button
      small
      color="error"
      tooltip="Collapse All"
      icon-id="mdi-arrow-collapse-all"
      @click="$emit('close:all')"
    />
    <generic-icon-button
      small
      color="primary"
      tooltip="Expand All"
      icon-id="mdi-arrow-expand-all"
      @click="$emit('open:all')"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { GenericIconButton } from "@/components/common/button";
import { FlexBox } from "@/components/common/layout";

/**
 * Displays section controls.
 *
 * @emits-1 `open:all` - On open all.
 * @emits-2 `close:all` - On close all.
 */
export default Vue.extend({
  name: "SectionControls",
  components: { FlexBox, GenericIconButton },
});
</script>
