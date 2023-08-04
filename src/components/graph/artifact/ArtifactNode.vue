<template>
  <cy-element
    :definition="definition"
    :style="style"
    :data-cy="dataCy"
    :data-cy-name="props.artifact.name"
    @add="handleAdd"
  >
    <node-display
      separator
      :color="color"
      variant="artifact"
      :title="props.artifact.type"
      :subtitle="displayName"
      :selected="selected"
      @click="handleSelect"
    >
      <separator
        v-if="showDelta"
        :color="deltaColor"
        class="cy-node-delta-chip"
      />
    </node-display>

    <node-display
      v-if="showHiddenChildren"
      :color="color"
      variant="footer"
      :selected="selected"
      @click="subtreeStore.showSubtree(id)"
      @mousedown.stop
      @mouseup.stop
    >
      <flex-box align="center" justify="center" :class="deltaClassName">
        <icon variant="down" size="sm" />
        <typography :value="hiddenChildrenLabel" />
      </flex-box>
      <flex-box v-if="showDelta" class="cy-node-delta-chip">
        <separator
          v-for="childColor in childDeltaColors"
          :key="childColor"
          :color="childColor"
          class="cy-node-delta-child-chip"
        />
      </flex-box>
      <q-tooltip :delay="300">Show children</q-tooltip>
    </node-display>

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
          tooltip="View related artifacts"
          icon="view-tree"
          @click="documentStore.addDocumentOfNeighborhood(props.artifact)"
        />
        <icon-button
          v-if="showHiddenChildren && hasSubtree"
          tooltip="Show subtree"
          icon="group-open-all"
          @click="subtreeStore.showSubtree(id)"
        />
        <icon-button
          v-else-if="hasSubtree"
          tooltip="Hide subtree"
          icon="group-close-all"
          @click="subtreeStore.hideSubtree(id)"
        />

        <separator v-if="displayEditing" class="full-width q-my-xs" />

        <icon-button
          v-if="displayEditing"
          tooltip="Add parent"
          icon="trace"
          color="primary"
          :rotate="-90"
          @click="
            appStore.openTraceCreatorTo({
              type: 'source',
              artifactId: id,
            })
          "
        />
        <icon-button
          v-if="displayEditing"
          tooltip="Add child"
          icon="trace"
          color="primary"
          :rotate="90"
          @click="
            appStore.openTraceCreatorTo({
              type: 'target',
              artifactId: id,
            })
          "
        />
      </flex-box>
    </node-display>
  </cy-element>
</template>

<script lang="ts">
/**
 * Renders an artifact node within the graph.
 */
export default {
  name: "ArtifactNode",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  ArtifactCytoElement,
  ArtifactSchema,
  CytoCore,
  GraphElementType,
  GraphMode,
} from "@/types";
import { getEnumColor, isCodeArtifact } from "@/util";
import {
  useTheme,
  deltaStore,
  selectionStore,
  subtreeStore,
  layoutStore,
  documentStore,
  appStore,
  sessionStore,
  projectStore,
  timStore,
} from "@/hooks";
import { NodeDisplay } from "@/components/graph/display";
import {
  FlexBox,
  Icon,
  Typography,
  Separator,
  IconButton,
} from "@/components/common";
import { CyElement } from "../base";

const props = defineProps<{
  artifactsInView: string[];
  artifact: ArtifactSchema;
}>();

const { darkMode } = useTheme();

const displayEditing = computed(() =>
  sessionStore.isEditor(projectStore.project)
);

const id = computed(() => props.artifact.id);

const selected = computed(() => selectionStore.isArtifactInSelected(id.value));
const faded = computed(() => !props.artifactsInView.includes(id.value));
const hidden = computed(() =>
  subtreeStore.hiddenSubtreeNodes.includes(id.value)
);

const opacity = computed(() => (hidden.value ? 0 : faded.value ? 0.3 : 1));
const style = computed(
  () =>
    `opacity: ${opacity.value};` +
    (selected.value ? "z-index: 10;" : "z-index: 1;")
);

const displayName = computed(
  () =>
    (isCodeArtifact(props.artifact.name) &&
      props.artifact.name.split("/").pop()) ||
    props.artifact.name
);

const hasSubtree = computed(
  () => subtreeStore.getChildren(id.value).length > 0
);
const hiddenChildren = computed(() => subtreeStore.getHiddenChildren(id.value));
const hiddenChildrenLabel = computed(() =>
  hiddenChildren.value.length === 1
    ? "1 Hidden"
    : `${hiddenChildren.value.length} Hidden`
);
const showHiddenChildren = computed(() => hiddenChildren.value.length > 0);

const deltaState = computed(() => deltaStore.getArtifactDeltaType(id.value));
const hiddenChildDeltaStates = computed(() =>
  deltaStore.getArtifactDeltaStates(hiddenChildren.value)
);
const showDelta = computed(() => deltaStore.inDeltaView);
const deltaClassName = computed(() =>
  showDelta.value && hiddenChildren.value.length > 0
    ? "cy-node-delta-footer"
    : ""
);
const deltaColor = computed(() => getEnumColor(deltaState.value));
const childDeltaColors = computed(() =>
  hiddenChildDeltaStates.value.map(getEnumColor)
);

const typeColor = computed(() => timStore.getTypeColor(props.artifact.type));
const color = computed(() =>
  showDelta.value ? deltaColor.value : typeColor.value
);

const dataCy = computed(() =>
  selected.value ? "tree-node-selected" : "tree-node"
);

const definition = computed<ArtifactCytoElement>(() => {
  const { id, type, name } = props.artifact;

  return {
    data: {
      type: GraphElementType.node,
      graph: GraphMode.tree,
      id,

      artifactName: name,
      artifactType: type,

      dark: darkMode.value,
    },
  };
});

/**
 * Handles the add event to set this artifact's default position,
 * and highlight it if it is selected.
 */
function handleAdd(cy: CytoCore): void {
  cy.getElementById(id.value).layout(layoutStore.layoutOptions).run();

  if (id.value !== selectionStore.selectedArtifact?.id) return;

  selectionStore.selectArtifact(id.value);
}

/**
 * Selects an artifact and highlights its subtree,
 * or opens a new view of the artifact's subtree if the artifact is already selected.
 */
function handleSelect(): void {
  if (!selected.value) {
    selectionStore.selectArtifact(id.value);
  } else {
    documentStore.addDocumentOfNeighborhood({
      id: id.value,
      name: props.artifact.name,
    });
  }
}
</script>
