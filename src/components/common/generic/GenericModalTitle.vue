<template>
  <v-row justify="space-between" class="pb-1">
    <label>{{ title }}</label>
    <GenericIconButton
      tooltip="Close"
      @onClick="$emit('onClose')"
      icon-id="mdi-close"
    />
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import GenericIconButton from "./GenericIconButton.vue";

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
