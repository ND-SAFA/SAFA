<template>
  <v-flex class="d-flex justify-center">
    <generic-icon-button
      color="error"
      tooltip="Collapse All"
      icon-id="mdi-arrow-collapse-all"
      @click="$emit('close-all')"
    />
    <generic-icon-button
      color="primary"
      tooltip="Expand All"
      icon-id="mdi-arrow-expand-all"
      @click="$emit('open-all')"
    />
  </v-flex>
</template>

<script lang="ts">
import Vue from "vue";
import GenericIconButton from "@/components/common/generic/GenericIconButton.vue";

/**
 * Displays section controls.
 *
 * @emits-1 `open-all` - On left button click.
 * @emits-2 `close-all` - On right button click.
 */
export default Vue.extend({
  name: "section-controls",
  components: { GenericIconButton },
});
</script>
