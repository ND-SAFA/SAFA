<template>
  <cy-element
    :definition="definition"
    :style="style"
    :data-cy="dataCy"
    :data-cy-name="props.artifact.name"
    :data-cy-children="hiddenChildren.length"
    @add="handleAdd"
  >
    <artifact-node-display
      :artifact="props.artifact"
      :color="color"
      :delta-color="deltaColor"
      :selected="selected"
    />
    <artifact-node-footer
      :artifact="props.artifact"
      :color="color"
      :selected="selected"
      :hidden-children="hiddenChildren"
    />
    <artifact-node-actions
      :artifact="props.artifact"
      :color="color"
      :selected="selected"
      :hidden-children="hiddenChildren"
    />
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
  ArtifactNodeProps,
  CytoCore,
  GraphElementType,
  GraphMode,
} from "@/types";
import { getEnumColor } from "@/util";
import {
  useTheme,
  deltaStore,
  selectionStore,
  subtreeStore,
  layoutStore,
  timStore,
} from "@/hooks";
import { CyElement } from "@/components/graph/base";
import ArtifactNodeActions from "./ArtifactNodeActions.vue";
import ArtifactNodeFooter from "./ArtifactNodeFooter.vue";
import ArtifactNodeDisplay from "./ArtifactNodeDisplay.vue";

const props = defineProps<ArtifactNodeProps>();

const { darkMode } = useTheme();

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

const hiddenChildren = computed(() => subtreeStore.getHiddenChildren(id.value));

const deltaState = computed(() => deltaStore.getArtifactDeltaType(id.value));
const showDelta = computed(() => deltaStore.inDeltaView);

const deltaColor = computed(() => getEnumColor(deltaState.value));
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
      graph: "tree" as GraphMode,
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

  if (id.value !== selectionStore.selectedArtifactId) return;

  selectionStore.selectArtifact(id.value);
}
</script>
