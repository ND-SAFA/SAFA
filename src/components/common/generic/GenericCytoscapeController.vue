<template>
  <cytoscape
    id="cy-container"
    :config="cytoCoreGraph.config"
    :preConfig="preConfig"
    :afterCreated="afterCreated"
  >
    <slot name="elements" />
  </cytoscape>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { CytoCore, CytoCoreGraph } from "@/types";
import { logModule } from "@/store";

/**
 * Abstracts setting up a cytoscape instance and corresponding
 * plugins.
 *
 */
export default Vue.extend({
  props: {
    cytoCoreGraph: {
      type: Object as PropType<CytoCoreGraph>,
      required: true,
    },
  },
  methods: {
    preConfig(cy: CytoCore) {
      this.cytoCoreGraph.plugins.forEach((plugin) => {
        try {
          plugin.initialize(cy);
        } catch (e) {
          console.warn(`Plugin installation error: ${e}`);
        }
      });
    },
    async afterCreated(cy: CytoCore) {
      if (this.cytoCoreGraph.saveCy) {
        this.cytoCoreGraph.saveCy(cy);
      } else {
        logModule.onDevError(
          `Unable to save cytoscape instance in: ${this.cytoCoreGraph.name}`
        );
      }
      this.cytoCoreGraph.plugins.forEach((plugin) => {
        plugin.afterInit(cy);
      });
      this.cytoCoreGraph.afterInit(cy);
    },
  },
});
</script>
