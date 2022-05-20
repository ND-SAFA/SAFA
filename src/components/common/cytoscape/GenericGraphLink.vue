<template>
  <cy-element
    :definition="definition"
    v-on:click="$emit('click:right', traceDefinition)"
  />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactDeltaState, TraceCytoCoreElement, TraceLink } from "@/types";
import { deltaModule } from "@/store";

/**
 * Displays trace link edge.
 *
 * @emits `click:right` - On right click.
 */
export default Vue.extend({
  name: "TraceLink",
  props: {
    traceDefinition: {
      type: Object as PropType<TraceLink>,
      required: true,
    },
    count: Number,
    faded: Boolean,
  },
  computed: {
    /**
     * @return The delta state of this trace link.
     */
    linkDeltaState(): ArtifactDeltaState {
      if (!deltaModule.inDeltaView) {
        return ArtifactDeltaState.NO_CHANGE;
      }

      return (
        deltaModule.getTraceDeltaType(this.traceDefinition.traceLinkId) ||
        ArtifactDeltaState.NO_CHANGE
      );
    },
    /**
     * @return The trace link's data definition.
     */
    definition(): TraceCytoCoreElement {
      const { sourceId, targetId, traceLinkId } = this.traceDefinition;

      return {
        data: {
          ...this.traceDefinition,
          type: "edge",
          id: traceLinkId,
          // Reversed to show arrow toward parent.
          source: targetId,
          target: sourceId,
          count: this.count || 1,
          deltaType: this.linkDeltaState,
          faded: this.faded,
        },
        classes: sourceId === targetId ? ["loop"] : [],
      };
    },
  },
});
</script>
