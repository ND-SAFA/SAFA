<template>
  <v-tooltip bottom z-index="12" :disabled="text.length < 10">
    <template v-slot:activator="{ on, attrs }">
      <v-chip
        v-on="on"
        v-bind="attrs"
        small
        class="text-body-1"
        style="max-width: 200px"
      >
        <v-icon small>{{ icon }}</v-icon>
        <span class="text-ellipsis ml-1">{{ displayText }}</span>
      </v-chip>
    </template>
    <span>{{ displayText }}</span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue from "vue";
import { typeOptionsModule } from "@/store";
import { getArtifactTypePrintName } from "@/util";

/**
 * Renders a chip on an artifact table row.
 */
export default Vue.extend({
  name: "ArtifactTableChip",
  props: {
    text: String,
    displayIcon: Boolean,
  },
  computed: {
    /**
     * @return The icon to display on this chip.
     */
    icon(): string {
      return this.displayIcon
        ? typeOptionsModule.getArtifactTypeIcon(this.text)
        : "";
    },
    /**
     * @return The text to display on this chip.
     */
    displayText(): string {
      return this.displayIcon ? getArtifactTypePrintName(this.text) : this.text;
    },
  },
});
</script>
