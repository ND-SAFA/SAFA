<template>
  <v-btn outlined :color="titleColor" @click="$emit('click', name)">
    <span style="max-width: 100px; overflow: hidden; text-overflow: ellipsis">{{
      name
    }}</span>
  </v-btn>
</template>

<script lang="ts">
import { DeltaType } from "@/types";
import Vue, { PropType } from "vue";

/**
 * Displays delta information.
 *
 * @emits `click` (name: string) - On click.
 */
export default Vue.extend({
  props: {
    name: {
      type: String,
      required: true,
    },
    deltaType: {
      type: String as PropType<DeltaType>,
      required: true,
    },
  },
  computed: {
    titleColor(): string {
      switch (this.deltaType) {
        case "added":
          return "success";
        case "modified":
          return "info";
        case "removed":
          return "error";
        default:
          return "black";
      }
    },
  },
});
</script>
