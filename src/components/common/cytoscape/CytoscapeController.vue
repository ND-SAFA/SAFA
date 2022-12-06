<template>
  <cytoscape
    :id="id"
    class="cy-container"
    :config="cytoCoreGraph.config"
    :preConfig="preConfig"
    :afterCreated="afterCreated"
  >
    <slot v-if="initialized" name="elements" />
  </cytoscape>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { CytoCore, CytoCoreGraph } from "@/types";
import { logStore } from "@/hooks";

/**
 * Abstracts setting up a cytoscape instance and corresponding plugins.
 */
export default Vue.extend({
  name: "CytoscapeController",
  props: {
    cytoCoreGraph: {
      type: Object as PropType<CytoCoreGraph>,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      initialized: false,
    };
  },
  methods: {
    /**
     * Initializes all plugins.
     * @param cy - The cytoscape instance.
     */
    preConfig(cy: CytoCore) {
      this.cytoCoreGraph.plugins.forEach((plugin) => {
        try {
          plugin.initialize(cy);
        } catch (e) {
          logStore.onDevError(`Plugin installation error: ${e}`);
        }
      });
    },
    /**
     * Finalizes all plugins.
     * @param cy - The cytoscape instance.
     */
    async afterCreated(cy: CytoCore) {
      if (this.cytoCoreGraph.saveCy) {
        this.cytoCoreGraph.saveCy(cy);
      } else {
        logStore.onDevError(
          `Unable to save cytoscape instance in: ${this.cytoCoreGraph.name}`
        );
      }
      this.cytoCoreGraph.plugins.forEach((plugin) => {
        plugin.afterInit(cy);
      });
      this.cytoCoreGraph.afterInit(cy);
      this.initialized = true;
    },
  },
});
</script>
