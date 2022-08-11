<template>
  <div class="d-flex justify-space-between full-width align-center">
    <typography :value="title" color="white" />
    <generic-icon-button
      tooltip="Close"
      icon-id="mdi-close"
      color="white"
      @click="$emit('close')"
    />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import GenericIconButton from "../generic/GenericIconButton.vue";
import Typography from "@/components/common/display/Typography.vue";

/**
 * Displays a generic modal title.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "GenericModalTitle",
  components: {
    Typography,
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
