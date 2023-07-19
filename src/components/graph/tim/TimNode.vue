<template>
  <cy-element3 :definition="definition">
    <q-card
      flat
      bordered
      class="cy-node cy-node-tim q-px-lg q-py-md"
      :style="cardStyle"
    >
      <div class="cy-node-title">
        <typography variant="subtitle" :value="props.artifactType" bold />
      </div>
      <separator :style="separatorStyle" class="cy-node-separator q-my-sm" />
      <typography variant="subtitle" :value="countLabel" />
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
import { Typography, Separator } from "@/components/common";
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
const cardStyle = computed(() => `border-color: ${typeColor.value};`);
const separatorStyle = computed(() => `background-color: ${typeColor.value};`);

const countLabel = computed(() =>
  props.count === 1 ? "1 Artifact" : `${props.count} Artifacts`
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
