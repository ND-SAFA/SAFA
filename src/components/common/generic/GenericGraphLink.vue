<template>
  <cy-element
    :definition="definition"
    v-on:click="$emit('right-click', traceDefinition)"
  />
</template>

<script lang="ts">
import { Link } from "@/types";
import Vue, { PropType } from "vue";

/**
 * Displays trace link edge.
 *
 * @emits `right-click` - On right click.
 */
export default Vue.extend({
  name: "trace-link",
  props: {
    traceDefinition: Object as PropType<Link>,
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
