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
    count: {
      type: Number,
      required: false,
    },
  },
  computed: {
    definition() {
      const source = this.traceDefinition.source;
      const target = this.traceDefinition.target;
      const id = `${source}-${target}`;
      const count = this.count ? this.count : 1;
      return {
        data: {
          ...this.traceDefinition,
          id,
          source: target, //see comment header for explanation
          target: source,
          count,
        },
      };
    },
  },
});
</script>
