<template>
  <cy-element
    :definition="definition"
    :style="style"
    data-cy="tim-node"
    :data-cy-name="props.artifactType"
  >
    <node-display
      separator
      :color="color"
      variant="tim"
      :title="props.artifactType"
      :subtitle="countLabel"
      :selected="selected"
      @click="handleSelect"
    />

    <node-display
      v-if="selected"
      :color="color"
      variant="sidebar"
      :selected="selected"
      @mousedown.stop
      @mouseup.stop
    >
      <flex-box column>
        <icon-button
          tooltip="View artifacts"
          icon="view-tree"
          @click="viewsStore.addDocumentOfTypes([props.artifactType])"
        />
        <separator v-if="displayActions" class="full-width q-my-xs" />
        <icon-button
          v-if="displayActions && ENABLED_FEATURES.GENERATE_SUMMARIES"
          tooltip="Summarize artifacts"
          icon="generate-summaries"
          color="gradient"
          data-cy="button-summarize-artifact"
          @click="appStore.openDetailsPanel('summarizeArtifact')"
        />
        <icon-button
          v-if="displayActions"
          tooltip="Generate parents"
          icon="generate-artifacts"
          color="gradient"
          @click="appStore.openDetailsPanel('generateArtifact')"
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
import {
  GraphElementType,
  GraphMode,
  TimNodeCytoElement,
  TimNodeProps,
} from "@/types";
import { ENABLED_FEATURES, sanitizeNodeId } from "@/util";
import {
  timStore,
  appStore,
  selectionStore,
  useTheme,
  permissionStore,
  viewsStore,
} from "@/hooks";
import { CyElement } from "@/components/graph/base";
import { NodeDisplay } from "@/components/graph/display";
import { FlexBox, IconButton, Separator } from "@/components";

const props = defineProps<TimNodeProps>();

const { darkMode } = useTheme();

const displayActions = computed(() =>
  permissionStore.isAllowed("project.generate")
);

const selected = computed(
  () => selectionStore.selectedArtifactLevelType === props.artifactType
);

const style = computed(() => (selected.value ? "z-index: 10;" : "z-index: 1;"));

const color = computed(() => timStore.getTypeColor(props.artifactType));

const countLabel = computed(() =>
  props.count < 0
    ? "1 Import"
    : props.count === 1
      ? "1 Artifact"
      : `${props.count} Artifacts`
);

const definition = computed<TimNodeCytoElement>(() => ({
  data: {
    type: GraphElementType.node,
    graph: "tim" as GraphMode,
    id: sanitizeNodeId(props.artifactType),

    artifactType: props.artifactType,

    dark: darkMode.value,
  },
}));

/**
 * Selects this artifact level.
 */
function handleSelect(): void {
  if (props.hideActions) return;

  if (!selected.value) {
    selectionStore.selectArtifactLevel(props.artifactType);
  } else {
    viewsStore.addDocumentOfTypes([props.artifactType]);
  }
}
</script>
