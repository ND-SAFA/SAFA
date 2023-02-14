<template>
  <cytoscape3
    :id="id"
    class="cy-container neutral-bg"
    :config="props.cytoCoreGraph.config"
    :pre-config="preConfig"
    :after-created="afterCreated"
  >
    <slot v-if="initialized" name="elements" />
  </cytoscape3>
</template>

<script lang="ts">
/**
 * Abstracts setting up a cytoscape instance and corresponding plugins.
 */
export default {
  name: "CytoscapeController",
};
</script>

<script setup lang="ts">
import { defineProps, ref } from "vue";
import { CytoCore, CytoCoreGraph, CytoCorePlugin } from "@/types";
import { logStore } from "@/hooks";
import { Cytoscape3 } from "./base";

const props = defineProps<{
  cytoCoreGraph: CytoCoreGraph;
  id: string;
}>();

const initialized = ref(false);

/**
 * Initializes all plugins.
 * @param cy - The cytoscape instance.
 */
function preConfig(cy: CytoCore) {
  props.cytoCoreGraph.plugins.forEach((plugin: CytoCorePlugin) => {
    try {
      plugin.initialize(cy);
    } catch (e) {
      logStore.onDevError(`Plugin installation error: ${e}`);
    }
  });
}

/**
 * Finalizes all plugins.
 * @param cy - The cytoscape instance.
 */
async function afterCreated(cy: CytoCore) {
  if (props.cytoCoreGraph.saveCy) {
    props.cytoCoreGraph.saveCy(cy);
  } else {
    logStore.onDevError(
      `Unable to save cytoscape instance in: ${props.cytoCoreGraph.name}`
    );
  }
  props.cytoCoreGraph.plugins.forEach((plugin: CytoCorePlugin) => {
    plugin.afterInit(cy);
  });
  props.cytoCoreGraph.afterInit(cy);
  initialized.value = true;
}
</script>
