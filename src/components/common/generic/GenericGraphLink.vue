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
  name: "trace-link",
  props: {
    traceDefinition: Object as PropType<TraceLink>,
    count: {
      type: Number,
      required: false,
    },
  },
  computed: {
    selector() {
      const { traceLinkId } = this.traceDefinition;

      return deltaModule.getTraceDeltaType(traceLinkId);
    },
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
        },
        classes: sourceId === targetId ? ["loop"] : [],
      };
    },
  },
});
</script>
