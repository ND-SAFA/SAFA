<template>
  <flex-box full-width justify="space-between" align="center">
    <typography :value="title" color="white" />
    <generic-icon-button
      tooltip="Close"
      icon-id="mdi-close"
      color="white"
      data-cy="button-close"
      @click="$emit('close')"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import GenericIconButton from "../generic/GenericIconButton.vue";
import Typography from "@/components/common/display/Typography.vue";
import FlexBox from "@/components/common/display/FlexBox.vue";

/**
 * Displays a generic modal title.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "GenericModalTitle",
  components: {
    FlexBox,
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
