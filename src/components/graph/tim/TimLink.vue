<template>
  <cy-element3 :definition="definition" />
</template>

<script lang="ts">
/**
 * Displays link between two artifact layers.
 */
export default {
  name: "TimLink",
};
</script>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import { useTheme } from "vuetify";
import { GraphElementType, GraphMode, TimEdgeCytoElement } from "@/types";
import { getTraceId } from "@/util";
import { CyElement3 } from "../base";

const props = defineProps<{
  sourceType: string;
  targetType: string;
  count: number;
  generated?: boolean;
}>();

const theme = useTheme();
const darkMode = computed(() => theme.global.current.value.dark);

const definition = computed<TimEdgeCytoElement>(() => ({
  data: {
    type: GraphElementType.edge,
    graph: GraphMode.tim,
    id: getTraceId(props.sourceType, props.targetType),
    // Reversed to show arrow toward parent.
    source: props.targetType,
    target: props.sourceType,
    count: props.count,
    label: props.count === 1 ? `1 Link` : `${props.count} Links`,
    dark: darkMode.value,
    generated: props.generated,
  },
  classes: props.sourceType === props.targetType ? ["loop"] : [],
}));
</script>
