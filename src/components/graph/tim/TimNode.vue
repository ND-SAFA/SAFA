<template>
  <cy-element3 :definition="definition" />
</template>

<script lang="ts">
/**
 * Renders a TIM node within the graph.
 */
export default {
  name: "TimNode",
};
</script>

<script setup lang="ts">
import { defineProps, computed } from "vue";
import { useTheme } from "vuetify";
import { GraphMode, GraphElementType, TimNodeCytoElement } from "@/types";
import { CyElement3 } from "../base";

const props = defineProps<{
  artifactType: string;
  count: number;
}>();

const theme = useTheme();
const darkMode = computed(() => theme.global.current.value.dark);

const definition = computed<TimNodeCytoElement>(() => ({
  data: {
    type: GraphElementType.node,
    graph: GraphMode.tim,
    id: props.artifactType.replace(/ /g, ""),
    artifactType: props.artifactType,
    count: props.count,
    dark: darkMode.value,
  },
}));
</script>
