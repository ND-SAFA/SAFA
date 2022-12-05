<template>
  <flex-box
    full-width
    justify="space-between"
    align="center"
    data-cy="modal-title"
  >
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
import { Typography } from "@/components/common/display";
import { GenericIconButton } from "@/components/common/button";
import { FlexBox } from "@/components/common/layout";

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
