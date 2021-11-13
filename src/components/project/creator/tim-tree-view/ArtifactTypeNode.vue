<template>
  <cy-element :definition="definition" />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Artifact, CytoCoreElementDefinition } from "@/types";
import { ArtifactPanel } from "@/components/project/creator/uploaders";

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
    definition(): CytoCoreElementDefinition {
      return {
        data: {
          id: this.type,
          type: "node",
        },
      };
    },
  },
});
</script>
