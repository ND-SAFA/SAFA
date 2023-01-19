<template>
  <cy-element :definition="definition" />
</template>

<script lang="ts">
import Vue from "vue";
import { GraphElementType, GraphMode, TimEdgeCytoElement } from "@/types";
import { getTraceId } from "@/util";

/**
 * Displays link between two artifact layers.
 */
export default Vue.extend({
  name: "TimLink",
  props: {
    source: {
      type: String,
      required: true,
    },
    target: {
      type: String,
      required: true,
    },
    count: {
      type: Number,
      required: true,
    },
  },
  computed: {
    /**
     * @return The TIM edge's data definition.
     */
    definition(): TimEdgeCytoElement {
      return {
        data: {
          type: GraphElementType.edge,
          graph: GraphMode.tim,
          id: getTraceId(this.source, this.target),
          // Reversed to show arrow toward parent.
          source: this.target,
          target: this.source,
          count: this.count,
        },
        classes: this.source === this.target ? ["loop"] : [],
      };
    },
  },
});
</script>
