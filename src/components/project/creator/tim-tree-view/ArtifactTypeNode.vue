<template>
  <cy-element :definition="definition" />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactPanel, TimNodeDefinition } from "@/types";

/**
 * The node representing an artifact type in the tim tree.
 */
export default Vue.extend({
  name: "ArtifactTypeNode",
  props: {
    artifactPanel: {
      type: Object as PropType<ArtifactPanel>,
      required: true,
    },
  },
  computed: {
    /**
     * @return The artifact tim node to render.
     */
    definition(): TimNodeDefinition {
      return {
        data: {
          id: this.artifactPanel.projectFile.type,
          type: "node",
          count: this.artifactPanel.projectFile.artifacts.length,
        },
      };
    },
  },
});
</script>
