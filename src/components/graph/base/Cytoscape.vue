<template>
  <div ref="container">
    <slot />
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  defineProps,
  withDefaults,
  provide,
  onMounted,
  defineEmits,
} from "vue";
import cytoscape, { CytoscapeOptions, Core, EventObject } from "cytoscape";
import { CytoEvent } from "@/types";

const props = withDefaults(
  defineProps<{
    config: CytoscapeOptions;
    preConfig?: (x: any) => void;
    afterCreated?: (x: any) => void;
  }>(),
  {
    preConfig: (x: any) => {},
    afterCreated: (x: any) => {},
  }
);

const emit = defineEmits<{
  (e: CytoEvent, event: EventObject): void;
}>();

const container = ref<HTMLElement | null>(null);
const instance = ref<Core | undefined>(undefined);
const resolve = ref<(value: PromiseLike<Core> | Core) => void>(() => {});
const reject = ref<(reason?: any) => void>(() => {});

provide(
  "cy",
  new Promise<Core>((res, rej) => {
    resolve.value = res;
    reject.value = rej;
  })
);

onMounted(() => {
  // create a vue independent element
  container.value?.setAttribute("id", "cytoscape-div");
  container.value?.setAttribute("width", "100%");
  container.value?.setAttribute("style", "min-height: 600px;");

  // apply lifecycle hooks
  if (props.preConfig) props.preConfig(cytoscape);

  // create cytoscape instance
  const cyInstance = cytoscape({ container: container.value, ...props.config });

  // register all the component events as cytoscape ones
  for (const eventType of Object.values(CytoEvent)) {
    cyInstance?.on(eventType, (event: EventObject) => {
      emit(eventType, event);
    });
  }

  instance.value = cyInstance;

  // resolve the promise with the object created
  resolve.value(cyInstance);

  if (props.afterCreated) props.afterCreated(cyInstance);
});
</script>
