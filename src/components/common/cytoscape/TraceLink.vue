<template>
  <cy-element
    :definition="definition"
    v-on:click="$emit('click:right', trace)"
  />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  ArtifactDeltaState,
  GraphElementType,
  GraphMode,
  TraceCytoCoreElement,
  TraceLinkSchema,
} from "@/types";
import { deltaStore } from "@/hooks";

/**
 * Displays trace link edge between artifacts.
 *
 * @emits `click:right` (TraceLinkSchema) - On right click.
 */
export default Vue.extend({
  name: "GraphLink",
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
    definition(): TraceCytoCoreElement {
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
