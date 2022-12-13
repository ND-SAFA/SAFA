<template>
  <v-chip v-if="doRender" small class="mr-1" :color="color" outlined>
    <typography :value="text" inherit-color />
  </v-chip>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactSchema, ArtifactDeltaState } from "@/types";
import { capitalize, getBackgroundColor } from "@/util";
import { deltaStore } from "@/hooks";
import { Typography } from "@/components/common";

/**
 * Renders a chip for the delta state of this artifact.
 */
export default Vue.extend({
  name: "ArtifactTableDeltaChip",
  components: { Typography },
  props: {
    artifact: Object as PropType<ArtifactSchema>,
  },
  computed: {
    /**
     * @return The delta state of this artifact.
     */
    deltaState(): ArtifactDeltaState {
      return deltaStore.getArtifactDeltaType(this.artifact.id);
    },
    /**
     * @return Whether to render this delta state chip.
     */
    doRender(): boolean {
      return this.deltaState !== ArtifactDeltaState.NO_CHANGE;
    },
    /**
     * @return The text to display on this chip.
     */
    text(): string {
      return capitalize(this.deltaState);
    },
    /**
     * @return The color to display for this chip.
     */
    color(): string {
      return getBackgroundColor(this.deltaState, this.$vuetify.theme.dark);
    },
  },
});
</script>
