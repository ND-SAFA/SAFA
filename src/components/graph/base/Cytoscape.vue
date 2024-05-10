<template>
  <div :id="id" ref="container" :class="className">
    <slot v-if="initialized" />
    <cy-context-menu v-if="initialized">
      <slot name="context-menu" />
    </cy-context-menu>
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
import { ref, provide, onMounted, onBeforeUnmount, computed } from "vue";
import cytoscape, { EventObject } from "cytoscape";
import { CytoCore, CytoEvent, CytoscapeProps } from "@/types";
import { logStore } from "@/hooks";
import CyContextMenu from "./CyContextMenu.vue";

const props = defineProps<CytoscapeProps>();

const emit = defineEmits<{
  (e: "click", event: EventObject): void;
}>();

const initialized = ref(false);
const container = ref<HTMLElement | null>(null);
const instance = ref<CytoCore | undefined>(undefined);
const resolve = ref<(value: PromiseLike<CytoCore> | CytoCore) => void>(
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  () => {}
);
// eslint-disable-next-line @typescript-eslint/no-empty-function
const reject = ref<() => void>(() => {});

const relTransform = ref("");

const className = computed(
  () => `cy-container bg-background ${props.class || ""}`
);

/**
 * Initializes all plugins.
 */
function beforeCreated(core: typeof cytoscape) {
  props.graph.plugins.forEach((plugin) => {
    try {
      plugin.initialize(core);
    } catch (e) {
      logStore.onDevError(`Plugin installation error: ${e}`);
    }
  });
}

/**
 * Finalizes all plugins.
 */
async function afterCreated(core: CytoCore) {
  if (props.graph.saveCy) {
    props.graph.saveCy(core);
  } else {
    logStore.onDevError(
      `Unable to save cytoscape instance in: ${props.graph.name}`
    );
  }

  props.graph.plugins.forEach((plugin) => {
    plugin.afterInit(core);
  });

  props.graph.afterInit(core);

  initialized.value = true;
}

/**
 * Initialized cytoscape to be synchronized with this component.
 */
function initCy(): void {
  // Set the container style.
  container.value?.setAttribute("id", props.id);
  container.value?.setAttribute("width", "100%");
  container.value?.setAttribute("style", "min-height: 600px;");

  // Apply lifecycle hooks.
  beforeCreated(cytoscape);

  // Create cytoscape instance.
  const cyInstance = cytoscape({
    container: container.value,
    ...props.graph.config,
  }) as CytoCore;

  instance.value = cyInstance;

  afterCreated(cyInstance);

  // Resolve the promise with the object created.
  resolve.value(cyInstance);
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
  new Promise<CytoCore>((res, rej) => {
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
