<template>
  <cy-element
    :definition="definition"
    data-cy="tim-node"
    :data-cy-name="props.artifactType"
  >
    <node-display
      separator
      :color="typeColor"
      variant="tim"
      :title="props.artifactType"
      :subtitle="countLabel"
    />
  </cy-element>
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
import { CyElement } from "@/components/graph/base";
import { NodeDisplay } from "@/components/graph/display";

const props = defineProps<{
  artifactType: string;
  count: number;
  icon?: string;
}>();

const { darkMode } = useTheme();

const typeColor = computed(
  () => typeOptionsStore.getArtifactLevel(props.artifactType)?.color || ""
);

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
