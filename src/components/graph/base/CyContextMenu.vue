<template>
  <div v-if="display" id="cy-context-menu" :style="style">
    <div
      style="
        background-color: red;
        width: 16px;
        height: 16px;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
      "
    ></div>
    <slot />
  </div>
</template>

<script lang="ts">
/**
 * A wrapper for managing a right click context menu on the graph.
 */
export default {
  name: "CyContextMenu",
};
</script>

<script setup lang="ts">
import { computed, inject, onBeforeUnmount, onMounted, ref } from "vue";
import { Core, EventObject } from "cytoscape";
import { CytoEvent } from "@/types";

const cy = inject<Promise<Core>>("cy");

const instance = ref<Core | undefined>(undefined);

const pos = ref<{ x: number; y: number } | undefined>();
const style = ref("");

const display = computed(() => !!pos.value);

/**
 * Sets up all event handlers.
 */
function listenForEmits(): void {
  const onRightClick = (event: EventObject) => {
    const oldPos = pos.value;
    const newPos = event.renderedPosition;

    if (oldPos?.x !== newPos.x || oldPos?.y !== newPos.y) {
      pos.value = { ...newPos };
      style.value = `
        z-index: 1000;
        position: absolute;
        left: ${newPos.x}px;
        top: ${newPos.y}px;
        right: auto;
        bottom: auto;
      `;
    }
  };

  const onOffClick = () => {
    pos.value = undefined;
    style.value = "";
  };

  instance.value?.on(CytoEvent.CXT_TAP, onRightClick);
  instance.value?.on(CytoEvent.CLICK, onOffClick);
}

/**
 * Listen for right click events to create the context menu.
 */
onMounted(() => {
  cy?.then((cy: Core) => {
    instance.value = cy;

    listenForEmits();
  });
});

/**
 * Cleanup event listeners on unmount.
 */
onBeforeUnmount(() => {
  instance.value?.off(CytoEvent.CXT_TAP);
  instance.value?.off(CytoEvent.CLICK);
});
</script>
