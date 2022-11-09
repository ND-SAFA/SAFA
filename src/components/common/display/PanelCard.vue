<template>
  <v-card outlined class="pa-2 mb-4" :style="style">
    <slot />
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { ThemeColors } from "@/util";

/**
 * Displays a card that contains panel content.
 */
export default Vue.extend({
  name: "PanelCard",
  computed: {
    /**
     * @return The style for this card.
     */
    style(): string {
      return `background-color: ${ThemeColors.lightGrey}`;
    },
  },
});
</script>
