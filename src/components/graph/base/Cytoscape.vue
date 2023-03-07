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
    id?: string;
    config: CytoscapeOptions;
    preConfig?: (cy: typeof cytoscape) => void;
    afterCreated?: (cy: Core) => void;
  }>(),
  {
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    preConfig: () => {},
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    afterCreated: () => {},
  }
);

const emit = defineEmits<{
  (e: CytoEvent, event: EventObject): void;
}>();

const container = ref<HTMLElement | null>(null);
const instance = ref<Core | undefined>(undefined);
// eslint-disable-next-line @typescript-eslint/no-empty-function
const resolve = ref<(value: PromiseLike<Core> | Core) => void>(() => {});
// eslint-disable-next-line @typescript-eslint/no-empty-function
const reject = ref<() => void>(() => {});

provide(
  "cy",
  new Promise<Core>((res, rej) => {
    resolve.value = res;
    reject.value = rej;
  })
);

onMounted(() => {
  // create a vue independent element
  container.value?.setAttribute("id", props.id || "cytoscape-div");
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
