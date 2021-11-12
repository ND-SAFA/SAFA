<template>
  <cytoscape
    id="cy-container"
    :config="graphDefinition.config"
    :preConfig="preConfig"
    :afterCreated="afterCreated"
  >
    <slot name="elements" />
  </cytoscape>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { CytoCore, CytoCoreGraph } from "@/types/cytoscape/core";

/**
 * Abstracts setting up a cytoscape instance and corresponding
 * plugins.
 */
export default Vue.extend({
  props: {
    graphDefinition: {
      type: Object as PropType<CytoCoreGraph>,
      required: true,
    },
  },
  methods: {
    preConfig(cy: CytoCore) {
      this.graphDefinition.plugins.forEach((plugin) => {
        try {
          plugin.plugin(cy);
        } catch (e) {
          console.log("plugin already installed");
        }
      });
    },
    async afterCreated(cy: CytoCore) {
      if (this.graphDefinition.saveCy) {
        this.graphDefinition.saveCy(cy);
      } else {
        console.warn(
          "Unable to save cytoscape instance in: ",
          this.graphDefinition.name
        );
      }
      this.graphDefinition.plugins.forEach((plugin) => {
        plugin.afterInit(cy);
      });
      this.graphDefinition.afterInit(cy);
    },
  },
});
</script>
