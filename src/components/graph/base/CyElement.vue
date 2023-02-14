<template>
  <div />
</template>

<script setup lang="ts">
import {
  ref,
  defineProps,
  withDefaults,
  watch,
  onBeforeUnmount,
  onMounted,
  inject,
  defineEmits,
} from "vue";
import {
  Selector,
  Core,
  ElementDefinition,
  EventObject,
  CollectionReturnValue,
  Position,
} from "cytoscape";
import { CytoEvent } from "@/types";

const props = withDefaults(
  defineProps<{
    definition: ElementDefinition;
    sync?: boolean;
  }>(),
  {
    sync: false,
  }
);

const emit = defineEmits<{
  (e: CytoEvent, event: EventObject): void;
}>();

const id = ref<string>(props.definition.data.id || "");
const selector = ref<Selector>(`#${id.value}`);
const instance = ref<Core | undefined>(undefined);

function add(): CollectionReturnValue | undefined {
  // register all the component events as cytoscape ones
  for (const eventType of Object.values(CytoEvent)) {
    instance.value?.on(eventType, selector.value, (event: EventObject) => {
      emit(eventType, event);
    });
  }

  // if sync is on, track position
  if (props.sync) {
    instance.value?.on("drag", selector.value, (event: EventObject) => {
      /*  Note: Cytoscape behaves badly when ele.position is an observer object. The underlying
          data may change, which adjust edge target coordinates, without re-drawing the node.

          In the definition below, and in the position watcher, JSON.parse(JSON.stringify())
          returns a raw object. Here, "definition.position" is an observer because of Vue, and
          event.target.position() seems to be an observer also. Without this strip, we end up with
          an observer of an observer after a drag event, one of which is stripped out in the
          watcher, creating the same problem we had initially.
      */

      // strip observers from the event position
      // update definition object
      // eslint-disable-next-line vue/no-mutating-props
      props.definition.position = JSON.parse(
        JSON.stringify(event.target.position())
      );
    });
  }

  // strip observers from the original definition
  let def = JSON.parse(JSON.stringify(props.definition));

  // add the element to cytoscape
  return instance.value?.add(def);
}

const cy = inject<Promise<Core>>("cy");

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
