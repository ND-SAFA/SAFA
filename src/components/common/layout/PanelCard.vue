<template>
  <v-card outlined :class="className">
    <slot />
  </v-card>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

/**
 * Displays a card that contains panel content.
 */
export default Vue.extend({
  name: "PanelCard",
  props: {
    color: {
      type: String as PropType<"primary" | "error" | "none">,
      default: "primary",
    },
  },
  computed: {
    /**
     * This card's class names.
     */
    className(): string {
      return `pa-4 mb-4 overflow-hidden ${this.color}-border`;
    },
  },
});
</script>
