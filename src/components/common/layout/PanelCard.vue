<template>
  <div class="pb-4 primary lighten-5">
    <v-card outlined :class="className">
      <slot />
    </v-card>
  </div>
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
      return `pa-4 overflow-hidden ${this.color}-border`;
    },
  },
});
</script>
