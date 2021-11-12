<template>
  <cy-element :definition="definition" />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Artifact, CytoCoreElementDefinition } from "@/types";

export default Vue.extend({
  name: "artifact-type-node",
  props: {
    type: {
      type: String,
      required: true,
    },
    artifacts: {
      type: Array as PropType<Artifact[]>,
      required: true,
    },
  },
  computed: {
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
