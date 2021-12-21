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
      const source = this.traceDefinition.source;
      const target = this.traceDefinition.target;
      const id = `${source}-${target}`;

      return deltaModule.getTraceDeltaType(id);
    },
    definition() {
      const source = this.traceDefinition.source;
      const target = this.traceDefinition.target;
      const id = `${source}-${target}`;
      const count = this.count ? this.count : 1;
      const traceType = deltaModule.getTraceDeltaType(id);

      return {
        data: {
          ...this.traceDefinition,
          id,
          // Reversed to show arrow toward parent.
          source: target,
          target: source,
          count,
        },
        classes: [`eh-delta-${traceType}`],
      };
    },
  },
});
</script>
