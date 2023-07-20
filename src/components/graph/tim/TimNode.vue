<template>
  <cy-element
    :definition="definition"
    data-cy="tim-node"
    :data-cy-name="props.artifactType"
    @click="handleSelect"
  >
    <node-display
      separator
      :color="color"
      variant="tim"
      :title="props.artifactType"
      :subtitle="countLabel"
      :selected="selected"
    />

    <node-display
      v-if="selected"
      :color="color"
      variant="sidebar"
      :selected="selected"
      @mouseenter="appStore.isGraphLock = true"
      @mouseleave="appStore.isGraphLock = false"
    >
      <flex-box column>
        <icon-button
          tooltip="View artifacts"
          icon="view-tree"
          @click="documentStore.addDocumentOfTypes([props.artifactType])"
        />
      </flex-box>
    </node-display>
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
import {
  appStore,
  documentStore,
  selectionStore,
  subtreeStore,
  typeOptionsStore,
  useTheme,
} from "@/hooks";
import { CyElement } from "@/components/graph/base";
import { NodeDisplay } from "@/components/graph/display";
import { FlexBox, IconButton, Separator } from "@/components";

const props = defineProps<{
  artifactType: string;
  count: number;
  icon?: string;
}>();

const { darkMode } = useTheme();

const selected = computed(
  () => selectionStore.selectedArtifactLevelType === props.artifactType
);

const color = computed(
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
    typeColor: color.value,
    icon: props.icon,
    dark: darkMode.value,
  },
}));

/**
 * Selects this artifact level.
 */
function handleSelect(): void {
  if (!selected.value) {
    selectionStore.selectArtifactLevel(props.artifactType);
  } else {
    documentStore.addDocumentOfTypes([props.artifactType]);
  }
}
</script>
