<template>
  <cytoscape
    :id="id"
    class="cy-container bg-neutral"
    :config="props.cytoCoreGraph.config"
    :pre-config="preConfig"
    :after-created="afterCreated"
    @click="emit('click', $event)"
  >
    <slot v-if="initialized" name="elements" />
  </cytoscape>
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
import { ref } from "vue";
import { EventObject } from "cytoscape";
import { CytoCore, CytoCoreGraph, CytoCorePlugin } from "@/types";
import { logStore } from "@/hooks";
import { Cytoscape } from "./base";

const props = defineProps<{
  cytoCoreGraph: CytoCoreGraph;
  id: string;
}>();

const emit = defineEmits<{
  (e: "click", event: EventObject): void;
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
