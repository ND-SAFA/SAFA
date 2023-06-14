<template>
  <cy-element3 :definition="definition" />
</template>

<script lang="ts">
/**
 * Displays trace link edges between artifact types.
 */
export default {
  name: "TimLink",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { GraphElementType, GraphMode, TimEdgeCytoElement } from "@/types";
import { getTraceId } from "@/util";
import { useTheme } from "@/hooks";
import { CyElement3 } from "../base";

const props = defineProps<{
  sourceType: string;
  targetType: string;
  count: number;
  generated?: boolean;
}>();

const { darkMode } = useTheme();

const definition = computed<TimEdgeCytoElement>(() => ({
  data: {
    type: GraphElementType.edge,
    graph: GraphMode.tim,
    id: getTraceId(props.sourceType, props.targetType).replace(/ /g, ""),
    // Reversed to show arrow toward parent.
    sourceType: props.targetType,
    targetType: props.sourceType,
    source: props.targetType.replace(/ /g, ""),
    target: props.sourceType.replace(/ /g, ""),
    count: props.count,
    label: props.count === 1 ? `1 Link` : `${props.count} Links`,
    dark: darkMode.value,
    generated: props.generated,
  },
  classes: props.sourceType === props.targetType ? "loop" : "",
}));
</script>
