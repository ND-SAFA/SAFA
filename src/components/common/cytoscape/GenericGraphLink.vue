<template>
  <cy-element
    :definition="definition"
    v-on:click="$emit('click:right', traceDefinition)"
  />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  ArtifactDeltaState,
  TraceCytoCoreElement,
  TraceLinkSchema,
} from "@/types";
import { deltaStore } from "@/hooks";

/**
 * Displays trace link edge.
 *
 * @emits `click:right` - On right click.
 */
export default Vue.extend({
  name: "TraceLink",
  props: {
    traceDefinition: {
      type: Object as PropType<TraceLinkSchema>,
      required: true,
    },
    graph: {
      type: String as PropType<"tim" | "artifact">,
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
      if (!deltaStore.inDeltaView) {
        return ArtifactDeltaState.NO_CHANGE;
      }

      return (
        deltaStore.getTraceDeltaType(this.traceDefinition.traceLinkId) ||
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
          graph: this.graph,
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
