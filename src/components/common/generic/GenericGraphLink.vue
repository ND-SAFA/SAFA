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
      const { sourceId, targetId } = this.traceDefinition;
      const id = `${sourceId}-${targetId}`;

      return deltaModule.getTraceDeltaType(id);
    },
    definition() {
      const { sourceId, targetId } = this.traceDefinition;
      const id = `${sourceId}-${targetId}`;
      const count = this.count ? this.count : 1;
      const traceType = deltaModule.getTraceDeltaType(id);
      const classes = [`eh-delta-${traceType}`];

      if (sourceId === targetId) {
        classes.push("loop");
      }

      return {
        data: {
          ...this.traceDefinition,
          id,
          // Reversed to show arrow toward parent.
          source: targetId,
          target: sourceId,
          count,
        },
        classes,
      };
    },
  },
});
</script>
