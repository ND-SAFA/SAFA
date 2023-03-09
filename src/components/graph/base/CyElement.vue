<template>
  <div />
</template>

<script setup lang="ts">
import { ref, watch, onBeforeUnmount, onMounted, inject } from "vue";
import {
  Selector,
  Core,
  ElementDefinition,
  CollectionReturnValue,
  Position,
} from "cytoscape";

const props = defineProps<{
  definition: ElementDefinition;
}>();

// const emit = defineEmits<{
//   (e: CytoEvent, event: EventObject): void;
// }>();

const id = ref<string>(props.definition.data.id || "");
const selector = ref<Selector>(`#${id.value}`);
const instance = ref<Core | undefined>(undefined);

const cy = inject<Promise<Core>>("cy");

function add(): CollectionReturnValue | undefined {
  // register all the component events as cytoscape ones
  // for (const eventType of Object.values(CytoEvent)) {
  //   instance.value?.on(eventType, selector.value, (event: EventObject) => {
  //     emit(eventType, event);
  //   });
  // }

  // strip observers from the original definition
  let def = JSON.parse(JSON.stringify(props.definition));

  // add the element to cytoscape
  return instance.value?.add(def);
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
    const ele = instance.value?.getElementById(id.value);

    ele?.position(JSON.parse(JSON.stringify(position)));
  },
  { deep: true }
);
</script>
