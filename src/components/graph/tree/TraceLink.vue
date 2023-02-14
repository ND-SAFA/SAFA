<template>
  <cy-element3 :definition="definition" />
</template>

<script lang="ts">
/**
 * Displays trace link edge between artifacts.
 */
export default {
  name: "TraceLink",
};
</script>

<script setup lang="ts">
import { useTheme } from "vuetify";
import { computed, defineProps } from "vue";
import { GraphElementType, GraphMode, TraceLinkSchema } from "@/types";
import { deltaStore } from "@/hooks";
import { CyElement3 } from "../base";

const props = defineProps<{
  trace: TraceLinkSchema;
  faded?: boolean;
}>();

const theme = useTheme();
const darkMode = computed(() => theme.global.current.value.dark);

const definition = computed(() => ({
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
    dark: darkMode.value,
  },
  classes: props.trace.sourceId === props.trace.targetId ? ["loop"] : [],
}));
</script>
