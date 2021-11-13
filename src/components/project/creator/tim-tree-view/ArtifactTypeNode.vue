<template>
  <cy-element :definition="definition" />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Artifact } from "@/types";
import { ArtifactPanel } from "@/components/project/creator/uploaders";
import { TypeNodeDefinitions } from "@/types/components/tim-tree";

/**
 * The node representing an artifact type in the tim tree.
 */
export default Vue.extend({
  name: "artifact-type-node",
  props: {
    artifactPanel: {
      type: Object as PropType<ArtifactPanel>,
      required: true,
    },
  },
  computed: {
    artifacts(): Artifact[] {
      return this.artifactPanel.projectFile.artifacts;
    },
    type(): string {
      return this.artifactPanel.projectFile.type;
    },
    count(): number {
      return this.artifacts.length;
    },
    definition(): TypeNodeDefinitions {
      return {
        data: {
          id: this.type,
          type: "node",
          count: this.count,
        },
      };
    },
  },
});
</script>
