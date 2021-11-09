<template>
  <v-row justify="space-between" class="pb-1">
    <label>{{ title }}</label>
    <GenericIconButton tooltip="Close" @onClick="$emit('onClose')">
      <template v-slot:icon>
        <v-icon id="close-button">mdi-close</v-icon>
      </template>
    </GenericIconButton>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import { GenericIconButton } from "@/components";

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
