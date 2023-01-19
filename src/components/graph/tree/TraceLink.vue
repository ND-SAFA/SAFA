<template>
  <cy-element :definition="definition" />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  ArtifactDeltaState,
  GraphElementType,
  GraphMode,
  TraceCytoElement,
  TraceLinkSchema,
} from "@/types";
import { deltaStore } from "@/hooks";

/**
 * Displays trace link edge between artifacts.
 */
export default Vue.extend({
  name: "TraceLink",
  props: {
    trace: {
      type: Object as PropType<TraceLinkSchema>,
      required: true,
    },
    faded: Boolean,
  },
  computed: {
    /**
     * @return The delta state of this trace link.
     */
    linkDeltaState(): ArtifactDeltaState {
      return deltaStore.getTraceDeltaType(this.trace.traceLinkId);
    },
    /**
     * @return The trace link's data definition.
     */
    definition(): TraceCytoElement {
      const { sourceId, targetId, traceLinkId, traceType, approvalStatus } =
        this.trace;

      return {
        data: {
          type: GraphElementType.edge,
          graph: GraphMode.tree,
          id: traceLinkId,
          // Reversed to show arrow toward parent.
          source: targetId,
          target: sourceId,
          deltaType: this.linkDeltaState,
          faded: this.faded,
          traceType,
          approvalStatus,
        },
        classes: sourceId === targetId ? ["loop"] : [],
      };
    },
  },
});
</script>
