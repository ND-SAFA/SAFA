<template>
  <cy-element :definition="definition" />
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
  TraceLinkSchema,
} from "@/types";
import { deltaStore, useTheme } from "@/hooks";
import { CyElement } from "../base";

const props = defineProps<{
  trace: TraceLinkSchema;
  faded?: boolean;
}>();

const { darkMode } = useTheme();

const definition = computed<TraceCytoElement>(() => ({
  data: {
    type: GraphElementType.edge,
    graph: GraphMode.tree,
    id: props.trace.traceLinkId,

    // Reversed to show arrow toward parent.
    source: props.trace.targetId,
    target: props.trace.sourceId,

    deltaType: deltaStore.getTraceDeltaType(props.trace.traceLinkId),
    faded: props.faded,
    traceType: props.trace.traceType,
    approvalStatus: props.trace.approvalStatus,
    score: props.trace.score,
    dark: darkMode.value,
  },
  classes: props.trace.sourceId === props.trace.targetId ? "loop" : "",
}));
</script>
