<template>
  <cy-element :definition="definition" />
</template>

<script lang="ts">
import Vue from "vue";
import { GraphMode, GraphElementType, TimNodeCytoElement } from "@/types";

/**
 * Renders a TIM node within the graph.
 */
export default Vue.extend({
  name: "TimNode",
  props: {
    artifactType: {
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
     * @return The cytoscape definition of this artifact.
     */
    definition(): TimNodeCytoElement {
      return {
        data: {
          type: GraphElementType.node,
          graph: GraphMode.tim,
          id: this.artifactType,
          artifactType: this.artifactType,
          count: this.count,
          dark: this.$vuetify.theme.dark,
        },
      };
    },
  },
});
</script>
