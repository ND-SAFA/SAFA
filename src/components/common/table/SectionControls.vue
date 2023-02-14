<template>
  <flex-box>
    <icon-button
      small
      color="error"
      tooltip="Collapse All"
      icon-id="mdi-arrow-collapse-all"
      @click="$emit('close:all')"
    />
    <icon-button
      small
      color="primary"
      tooltip="Expand All"
      icon-id="mdi-arrow-expand-all"
      @click="$emit('open:all')"
    />
  </flex-box>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { IconButton } from "@/components/common/button";
import { FlexBox } from "@/components/common/layout";

/**
 * Displays section controls.
 *
 * @emits-1 `open:all` - On open all.
 * @emits-2 `close:all` - On close all.
 */
export default defineComponent({
  name: "SectionControls",
  components: { FlexBox, IconButton },
});
</script>
