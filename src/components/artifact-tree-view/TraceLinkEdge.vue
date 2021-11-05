<template>
  <cy-element
    :definition="definition"
    v-on:click="$emit('onRightClick', traceDefinition)"
  />
</template>

<script lang="ts">
import { TraceLink } from "@/types";
import Vue, { PropType } from "vue";

export default Vue.extend({
  name: "trace-link",
  props: {
    traceDefinition: Object as PropType<TraceLink>,
  },
  computed: {
    definition() {
      const source = this.traceDefinition.source;
      const target = this.traceDefinition.target;
      const id = `${source}-${target}`;
      return {
        data: {
          ...this.traceDefinition,
          id,
          source: target, //see comment header for explanation
          target: source,
        },
      };
    },
  },
});
</script>
