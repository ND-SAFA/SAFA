<template>
  <div ref="container">
    <slot />
  </div>
</template>

<script lang="ts">
/**
 * A wrapper for managing a Cytoscape instance.
 */
export default {
  name: "Cytoscape",
};
</script>

<script setup lang="ts">
import { ref, withDefaults, provide, onMounted, onBeforeUnmount } from "vue";
import cytoscape, { CytoscapeOptions, Core, EventObject } from "cytoscape";
import { CytoEvent } from "@/types";

const props = withDefaults(
  defineProps<{
    id?: string;
    config: CytoscapeOptions;
    preConfig?: (cy: typeof cytoscape) => void;
    afterCreated?: (cy: Core) => void;
  }>(),
  {
    id: "cytoscape-div",
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    preConfig: () => {},
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    afterCreated: () => {},
  }
);

const emit = defineEmits<{
  (e: "click", event: EventObject): void;
}>();

const container = ref<HTMLElement | null>(null);
const instance = ref<Core | undefined>(undefined);
// eslint-disable-next-line @typescript-eslint/no-empty-function
const resolve = ref<(value: PromiseLike<Core> | Core) => void>(() => {});
// eslint-disable-next-line @typescript-eslint/no-empty-function
const reject = ref<() => void>(() => {});

const relTransform = ref("");

/**
 * Initialized cytoscape to be synchronized with this component.
 */
function initCy(): void {
  // Set the container style.
  container.value?.setAttribute("id", props.id);
  container.value?.setAttribute("width", "100%");
  container.value?.setAttribute("style", "min-height: 600px;");

  // Apply lifecycle hooks.
  if (props.preConfig) props.preConfig(cytoscape);

  // Create cytoscape instance.
  const cyInstance = cytoscape({ container: container.value, ...props.config });

  instance.value = cyInstance;

  // Resolve the promise with the object created.
  resolve.value(cyInstance);

  if (props.afterCreated) props.afterCreated(cyInstance);
}

/**
 * Adds a listener to track panning and zooming to translate where nodes are displayed.
 */
function listenForPanZoom(): void {
  const onPanZoom = (event: EventObject) => {
    const pan = event.cy.pan();
    const zoom = event.cy.zoom();

    relTransform.value = `translate(${pan.x}px,${pan.y}px) scale(${zoom})`;
  };

  instance.value?.on(CytoEvent.PAN_ZOOM, onPanZoom);
}

/**
 * Sets up all event handlers.
 */
function listenForEmits(): void {
  listenForPanZoom();

  instance.value?.on(CytoEvent.CLICK, (event) => emit("click", event));
}

provide(
  "cy",
  new Promise<Core>((res, rej) => {
    resolve.value = res;
    reject.value = rej;
  })
);

provide("relTransform", relTransform);

/**
 * Initialize cytoscape and event handlers on mount.
 */
onMounted(() => {
  initCy();
  listenForEmits();
});

/**
 * Clean up event handlers on unmount.
 */
onBeforeUnmount(() => {
  instance.value?.off(CytoEvent.PAN_ZOOM);
  instance.value?.off(CytoEvent.CLICK);
});
</script>
