<template>
  <cy-element :definition="definition" @click="handleSelect" />
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
import {
  GraphElementType,
  GraphMode,
  TimEdgeCytoElement,
  TimLinkProps,
} from "@/types";
import { getTraceId, sanitizeNodeId } from "@/util";
import { documentStore, selectionStore, useTheme } from "@/hooks";
import { CyElement } from "@/components/graph/base";

const props = defineProps<TimLinkProps>();

const { darkMode } = useTheme();

const definition = computed<TimEdgeCytoElement>(() => ({
  data: {
    type: GraphElementType.edge,
    graph: GraphMode.tim,
    id: sanitizeNodeId(getTraceId(props.sourceType, props.targetType)),

    // Reversed to show arrow toward parent.
    sourceType: props.targetType,
    targetType: props.sourceType,
    source: sanitizeNodeId(props.targetType),
    target: sanitizeNodeId(props.sourceType),

    count: props.count,
    label: props.count === 1 ? `1 Link` : `${props.count} Links`,
    dark: darkMode.value,
    generated: props.generated,
  },
  classes: props.sourceType === props.targetType ? "loop" : "",
}));

/**
 * Selects this trace matrix.
 */
function handleSelect(): void {
  if (
    selectionStore.selectedTraceMatrixTypes[0] !== props.targetType ||
    selectionStore.selectedTraceMatrixTypes[1] !== props.sourceType
  ) {
    selectionStore.selectTraceMatrix(props.sourceType, props.targetType);
  } else {
    documentStore.addDocumentOfTypes([props.sourceType, props.targetType]);
  }
}
</script>
