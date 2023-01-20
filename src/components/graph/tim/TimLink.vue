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
    sourceType: {
      type: String,
      required: true,
    },
    targetType: {
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
          id: getTraceId(this.sourceType, this.targetType),
          // Reversed to show arrow toward parent.
          source: this.targetType,
          target: this.sourceType,
          count: this.count,
          label: this.count === 1 ? `1 Link` : `${this.count} Links`,
          dark: this.$vuetify.theme.dark,
        },
        classes: this.sourceType === this.targetType ? ["loop"] : [],
      };
    },
  },
});
</script>
