<template>
  <v-row justify="space-between" class="pb-1">
    <label>{{ title }}</label>
    <generic-icon-button
      tooltip="Close"
      icon-id="mdi-close"
      @click="$emit('close')"
    />
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import GenericIconButton from "./GenericIconButton.vue";

/**
 * Displays a generic modal title.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "generic-modal-title",
  components: {
    GenericIconButton,
  },
  props: {
    title: {
      type: String,
      required: true,
    },
  },
});
</script>
