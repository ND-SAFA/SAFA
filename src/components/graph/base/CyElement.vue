<template>
  <div class="cy-node-position" :style="style">
    <slot />
  </div>
</template>

<script lang="ts">
/**
 * A wrapper for managing an element within a Cytoscape graph.
 */
export default {
  name: "CyElement",
};
</script>

<script setup lang="ts">
import {
  ref,
  watch,
  onBeforeUnmount,
  onMounted,
  inject,
  computed,
  Ref,
} from "vue";
import { Selector, Core, EventObject } from "cytoscape";
import { CyElementProps, CytoEvent, GraphElementType } from "@/types";

const props = defineProps<CyElementProps>();

const emit = defineEmits<{
  (e: "click", event: EventObject): void;
  (e: "add", cy: Core): void;
}>();

const cy = inject<Promise<Core>>("cy");
const relTransform = inject<Ref<string>>("relTransform");

const id = ref<string>(props.definition.data.id || "");
const selector = ref<Selector>(`#${id.value}`);
const instance = ref<Core | undefined>(undefined);

const pos = ref<{ x: number; y: number } | undefined>();
const absTransform = ref("");
const transformStyle = ref("");

const isNode = computed(
  () => props.definition.data.type === GraphElementType.node
);

const style = computed(() =>
  isNode.value ? `${transformStyle.value} ${props.style}` : props.style
);

/**
 * Creates this element within cytoscape.
 */
function addElement(): void {
  if (!instance.value) return;

  // Strip observers from the original definition.
  const def = JSON.parse(JSON.stringify(props.definition));

  // Add the element to cytoscape.
  const eles = instance.value.add(def);

  emit("add", instance.value!);

  if (id.value || !eles) return;

  id.value = eles[0].data().id;
  selector.value = `#${id.value}`;
}

/**
 * Adds a lister for movement of this node, updating the tracked position when it changes.
 */
function listenForMove(): void {
  if (!isNode.value) return;

  const onMove = (event: EventObject) => {
    const oldPos = pos.value;
    const newPos = event.target.position();

    if (oldPos?.x !== newPos.x || oldPos?.y !== newPos.y) {
      pos.value = { ...newPos };
      absTransform.value =
        `translate(-50%, -50%) ` +
        `translate(${newPos.x.toFixed(2)}px,${newPos.y.toFixed(2)}px)`;
    }
  };

  instance.value?.on(CytoEvent.POSITION, selector.value, onMove);
  // instance.value?.on(CytoEvent.POSITION_BOUNDS, selector.value, onMove);
}

/**
 * Sets up all event handlers.
 */
function listenForEmits(): void {
  listenForMove();

  instance.value?.on(CytoEvent.CLICK, selector.value, (event) =>
    emit("click", event)
  );
}

/**
 * Create the element within cytoscape and add listeners on mount.
 */
onMounted(() => {
  cy?.then((cy: Core) => {
    instance.value = cy;

    addElement();
    listenForEmits();
  });
});

/**
 * Cleanup event listeners on unmount.
 */
onBeforeUnmount(() => {
  instance.value?.remove(selector.value);
  instance.value?.off(CytoEvent.POSITION_BOUNDS, selector.value);
  instance.value?.off(CytoEvent.CLICK, selector.value);
});

/**
 * Update data when hard-coded data changes.
 */
watch(
  () => props.definition.data,
  (data) => {
    const ele = instance.value?.getElementById(id.value);

    ele?.data(data);
  },
  { deep: true }
);

/**
 * Update positions when hard-coded position changes.
 */
watch(
  () => props.definition.position,
  (position) => {
    if (!position) return;

    const ele = instance.value?.getElementById(id.value);

    ele?.position(JSON.parse(JSON.stringify(position)));
  },
  { deep: true }
);

/**
 * Update the computed style when the window or the element moves.
 */
watch(
  () => [absTransform.value, relTransform?.value],
  ([abs, rel]) => {
    const transform = `${rel} ${abs}`;

    transformStyle.value = `webkit-transform: ${transform}; ms-transform: ${transform}; transform: ${transform};`;
  }
);
</script>
