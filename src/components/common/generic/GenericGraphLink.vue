<template>
  <cy-element
    :definition="definition"
    v-on:click="$emit('click:right', traceDefinition)"
  />
</template>

<script lang="ts">
import { TraceLink } from "@/types";
import Vue, { PropType } from "vue";
import { deltaModule } from "@/store";

/**
 * Displays trace link edge.
 *
 * @emits `click:right` - On right click.
 */
export default Vue.extend({
  name: "TraceLink",
  props: {
    traceDefinition: Object as PropType<TraceLink>,
    count: {
      type: Number,
      required: false,
    },
    faded: Boolean,
  },
  computed: {
    /**
     * @return The trace link's selector.
     */
    selector() {
      const { traceLinkId } = this.traceDefinition;

      return deltaModule.getTraceDeltaType(traceLinkId);
    },
    /**
     * @return The trace link's data definition.
     */
    definition() {
      const { sourceId, targetId, traceLinkId } = this.traceDefinition;
      const count = this.count ? this.count : 1;
      const deltaType = deltaModule.getTraceDeltaType(traceLinkId);

      return {
        data: {
          ...this.traceDefinition,
          id: traceLinkId,
          // Reversed to show arrow toward parent.
          source: targetId,
          target: sourceId,
          count,
          deltaType,
          faded: this.faded,
        },
        classes: sourceId === targetId ? ["loop"] : [],
      };
    },
  },
});
</script>
