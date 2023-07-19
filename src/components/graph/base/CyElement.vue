<template>
  <div
    :style="
      isNode
        ? 'position: absolute; z-index: 1000;' +
          'webkit-transform-origin: top left; ms-transform-origin: top left; transform-origin: top left; ' +
          style
        : undefined
    "
  >
    <slot />
    <q-card v-if="isNode" flat bordered class="q-px-lg q-pt-md">
      <p>{{ props.definition.data.artifactName }}</p>
    </q-card>
  </div>
</template>

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
const style = ref("");

const cy = inject<Promise<Core>>("cy");
const relTransform = inject<Ref<string>>("relTransform");

const isNode = computed(
  () => props.definition.data.type === GraphElementType.node
);

/**
 * Creates this element within cytoscape.
 */
function addElement(): void {
  // Strip observers from the original definition.
  const def = JSON.parse(JSON.stringify(props.definition));

  // Add the element to cytoscape.
  const eles = instance.value?.add(def);

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

  instance.value?.on("position bounds", selector.value, onMove);
}

/**
 * Create the element within cytoscape and add listeners on mount.
 */
onMounted(() => {
  cy?.then((cy: Core) => {
    instance.value = cy;

    addElement();
    listenForMove();
  });
});

/**
 * Cleanup event listeners on unmount.
 */
onBeforeUnmount(() => {
  instance.value?.remove(selector.value);
  instance.value?.off("position bounds", selector.value);
});

/**
 * Update data when hard-coded data changes.
 */
watch(
  () => props.definition.data,
  (data: Record<string, unknown>) => {
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
  (position: Position | null = null) => {
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

    style.value = `webkit-transform: ${transform}; ms-transform: ${transform}; transform: ${transform};`;
  }
);
</script>
