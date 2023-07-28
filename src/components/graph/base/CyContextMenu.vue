<template>
  <div v-if="display" :style="style" class="cy-menu-position">
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
import {
  computed,
  inject,
  onBeforeUnmount,
  onMounted,
  provide,
  ref,
  watch,
} from "vue";
import { Core, EventObject } from "cytoscape";
import { useRoute } from "vue-router";
import { CytoEvent } from "@/types";
import { layoutStore } from "@/hooks";

const currentRoute = useRoute();

const cy = inject<Promise<Core>>("cy");

const instance = ref<Core | undefined>(undefined);

const pos = ref<{ x: number; y: number } | undefined>();
const style = ref("");

const display = computed(() => !!pos.value);

/**
 * Closes the context menu.
 */
function handleCloseMenu() {
  if (pos.value) {
    pos.value = undefined;
  }
  if (style.value) {
    style.value = "";
  }
}

/**
 * Sets up all event handlers.
 */
function listenForEmits(): void {
  const handleRightClick = (event: EventObject) => {
    const oldPos = pos.value;
    const newPos = event.renderedPosition;

    if (oldPos?.x !== newPos.x || oldPos?.y !== newPos.y) {
      pos.value = { ...newPos };
      style.value = `
        left: ${newPos.x}px;
        top: ${newPos.y}px;
      `;
    }
  };

  instance.value?.on(CytoEvent.CXT_TAP, handleRightClick);
  instance.value?.on(CytoEvent.CLICK, handleCloseMenu);
  instance.value?.on(CytoEvent.PAN_ZOOM, handleCloseMenu);
}

provide("menu-close", handleCloseMenu);

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
  instance.value?.off(CytoEvent.PAN_ZOOM);
});

watch(() => layoutStore.mode, handleCloseMenu);
watch(() => currentRoute.path, handleCloseMenu);
</script>
