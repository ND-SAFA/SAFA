<template>
  <v-chip
    v-if="doRender"
    small
    class="text-body-1 mr-1"
    :color="color"
    outlined
  >
    {{ text }}
  </v-chip>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Artifact, ArtifactDeltaState } from "@/types";
import { deltaModule } from "@/store";
import { capitalize, getBackgroundColor } from "@/util";

/**
 * Renders a chip for the delta state of this artifact.
 */
export default Vue.extend({
  name: "ArtifactTableDeltaChip",
  props: {
    artifact: Object as PropType<Artifact>,
  },
  computed: {
    /**
     * @return The delta state of this artifact.
     */
    deltaState(): ArtifactDeltaState {
      return deltaModule.getArtifactDeltaType(this.artifact.id);
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
      return getBackgroundColor(this.deltaState);
    },
  },
});
</script>
