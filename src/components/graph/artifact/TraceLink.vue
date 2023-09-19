<template>
  <cy-element :definition="definition" @click="handleSelect" />
</template>

<script lang="ts">
/**
 * Displays trace link edges between artifacts.
 */
export default {
  name: "TraceLink",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  GraphElementType,
  GraphMode,
  TraceCytoElement,
  TraceLinkProps,
} from "@/types";
import { deltaStore, selectionStore, useTheme } from "@/hooks";
import { CyElement } from "@/components/graph/base";

const props = defineProps<TraceLinkProps>();

const { darkMode } = useTheme();

const faded = computed(
  () =>
    !props.artifactsInView.includes(props.trace.targetId) ||
    !props.artifactsInView.includes(props.trace.sourceId)
);

const definition = computed<TraceCytoElement>(() => ({
  data: {
    type: GraphElementType.edge,
    graph: "tree" as GraphMode,
    id: props.trace.traceLinkId,

    // Reversed to show arrow toward parent.
    source: props.trace.targetId,
    target: props.trace.sourceId,

    deltaType: deltaStore.inDeltaView
      ? deltaStore.getTraceDeltaType(props.trace.traceLinkId)
      : undefined,
    faded: faded.value,
    traceType: props.trace.traceType,
    approvalStatus: props.trace.approvalStatus,
    score: props.trace.score,
    dark: darkMode.value,
  },
  classes: props.trace.sourceId === props.trace.targetId ? "loop" : "",
}));

/**
 * Selects this trace link.
 */
function handleSelect(): void {
  selectionStore.selectTraceLink(props.trace);
}
</script>
