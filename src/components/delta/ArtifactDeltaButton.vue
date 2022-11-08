<template>
  <v-btn outlined :color="titleColor" @click="$emit('click', name)">
    <span class="text-ellipsis" style="max-width: 180px; color: inherit">
      {{ name }}
    </span>
  </v-btn>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DeltaType } from "@/types";

/**
 * Displays an artifact delta button.
 *
 * @emits `click` (name: string) - On click.
 */
export default Vue.extend({
  name: "ArtifactDeltaButton",
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
    /**
     * The color to display for the button.
     */
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
