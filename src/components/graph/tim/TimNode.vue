<template>
  <cy-element3 :definition="definition">
    <q-card
      flat
      bordered
      class="q-px-lg q-py-md"
      :style="`border-color: ${typeColor}; border-width: 2px; text-align: center`"
    >
      <b>{{ props.artifactType }}</b>
      <q-separator :style="`background-color: ${typeColor}; height: 2px`" />
      <b>{{ count }} Artifacts</b>
    </q-card>
  </cy-element3>
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
import { computed } from "vue";
import { GraphMode, GraphElementType, TimNodeCytoElement } from "@/types";
import { sanitizeNodeId } from "@/util";
import { typeOptionsStore, useTheme } from "@/hooks";
import { CyElement3 } from "../base";

const props = defineProps<{
  artifactType: string;
  count: number;
  icon?: string;
}>();

const { darkMode } = useTheme();

const typeColor = computed(
  () => typeOptionsStore.getArtifactLevel(props.artifactType)?.color || ""
);

const definition = computed<TimNodeCytoElement>(() => ({
  data: {
    type: GraphElementType.node,
    graph: GraphMode.tim,
    id: sanitizeNodeId(props.artifactType),

    artifactType: props.artifactType,
    count: props.count,
    typeColor: typeColor.value,
    icon: props.icon,
    dark: darkMode.value,
  },
}));
</script>
