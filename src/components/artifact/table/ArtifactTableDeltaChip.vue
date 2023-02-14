<template>
  <v-chip v-if="doRender" small class="mr-1" :color="color" outlined>
    <typography :value="text" inherit-color />
  </v-chip>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "vue";
import { useTheme } from "vuetify";
import { ArtifactSchema, ArtifactDeltaState } from "@/types";
import { capitalize, getBackgroundColor } from "@/util";
import { deltaStore } from "@/hooks";
import { Typography } from "@/components/common";

/**
 * Renders a chip for the delta state of this artifact.
 */
export default defineComponent({
  name: "ArtifactTableDeltaChip",
  components: { Typography },
  props: {
    artifact: {
      type: Object as PropType<ArtifactSchema>,
      required: true,
    },
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
      const theme = useTheme();
      const darkMode = computed(() => theme.global.current.value.dark);

      return getBackgroundColor(this.deltaState, darkMode.value);
    },
  },
});
</script>
