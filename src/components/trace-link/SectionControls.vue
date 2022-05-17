<template>
  <div class="d-flex flex-row">
    <generic-icon-button
      color="error"
      tooltip="Collapse All"
      icon-id="mdi-arrow-collapse-all"
      @click="$emit('close:all')"
    />
    <generic-icon-button
      color="primary"
      tooltip="Expand All"
      icon-id="mdi-arrow-expand-all"
      @click="$emit('open:all')"
    />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { GenericIconButton } from "@/components/common";

/**
 * Displays section controls.
 *
 * @emits-1 `open:all` - On left button click.
 * @emits-2 `close:all` - On right button click.
 */
export default Vue.extend({
  name: "SectionControls",
  components: { GenericIconButton },
});
</script>
