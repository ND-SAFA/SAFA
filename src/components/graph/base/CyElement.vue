<template>
  <div
    :style="
      isNode
        ? 'position: absolute; ' +
          // 'webkitTransformOrigin: top left; msTransformOrigin: top left; transformOrigin: top left;' +
          'background: red; height: 4px; width: 4px; z-index: 1000; ' +
          style
        : undefined
    "
  />
</template>

<script setup lang="ts">
import { ref, watch, onBeforeUnmount, onMounted, inject, computed } from "vue";
import {
  Selector,
  Core,
  ElementDefinition,
  CollectionReturnValue,
  Position,
  EventObject,
} from "cytoscape";
import { GraphElementType } from "@/types";

const props = defineProps<{
  definition: ElementDefinition;
}>();

const id = ref<string>(props.definition.data.id || "");
const selector = ref<Selector>(`#${id.value}`);
const instance = ref<Core | undefined>(undefined);
const pos = ref<{ x: number; y: number } | undefined>();
const absTransform = ref("");
const relTransform = ref("");
const style = ref("");

const cy = inject<Promise<Core>>("cy");

const isNode = computed(
  () => props.definition.data.type === GraphElementType.node
);

function add(): CollectionReturnValue | undefined {
  listenForMove();
  listenForPanZoom();

  // strip observers from the original definition
  const def = JSON.parse(JSON.stringify(props.definition));

  // add the element to cytoscape
  return instance.value?.add(def);
}

function listenForMove(): void {
  if (!isNode.value) return;

  const onMove = (event: EventObject) => {
    const oldPos = pos.value;
    const newPos = event.target.position();

    if (oldPos?.x !== newPos.x || oldPos?.y !== newPos.y) {
      console.log("moving", selector.value, newPos);

      absTransform.value = `translate(${newPos.x.toFixed(
        2
      )}px,${newPos.y.toFixed(2)}px)`;
      pos.value = { ...newPos };
    }
  };

  instance.value?.on("position bounds", selector.value, onMove);

  // TODO: cleanup listener on unmount
}

function listenForPanZoom(): void {
  if (!isNode.value) return;

  const onPanZoom = (event: EventObject) => {
    const pan = event.cy.pan();
    const zoom = event.cy.zoom();

    console.log("panning", pan, zoom);

    relTransform.value = `translate(${pan.x}%,${pan.y}%) scale(${zoom})`;
  };

  instance.value?.on("pan zoom", onPanZoom);

  // TODO: cleanup listener on unmount
}

onMounted(() => {
  cy?.then((cy: Core) => {
    instance.value = cy;

    const eles = add();

    if (id.value || !eles) return;

    id.value = eles[0].data().id;
    selector.value = `#${id.value}`;
  });
});

onBeforeUnmount(() => {
  instance.value?.remove(selector.value);
});

watch(
  () => props.definition.data,
  (data: Record<string, unknown>) => {
    const ele = instance.value?.getElementById(id.value);

    ele?.data(data);
  },
  { deep: true }
);

watch(
  () => props.definition.position,
  (position: Position | null = null) => {
    if (!position) return;

    const ele = instance.value?.getElementById(id.value);

    ele?.position(JSON.parse(JSON.stringify(position)));
  },
  { deep: true }
);

watch(
  () => [absTransform.value, relTransform.value],
  ([abs, rel]) => {
    const transform = `${rel} ${abs}`;

    console.log("updating style", selector.value, transform);

    style.value = `webkitTransform: ${transform}; msTransform: ${transform}; transform: ${transform};`;
  }
);
</script>
