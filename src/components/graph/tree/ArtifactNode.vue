<template>
  <cy-element :definition="definition">
    <node-display
      :color="typeColor"
      :variant="GraphMode.tree"
      :title="props.artifact.type"
      :subtitle="props.artifact.name"
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
  ArtifactSchema,
  GraphElementType,
  GraphMode,
} from "@/types";
import { isCodeArtifact } from "@/util";
import {
  useTheme,
  deltaStore,
  selectionStore,
  subtreeStore,
  warningStore,
  typeOptionsStore,
} from "@/hooks";
import { NodeDisplay } from "@/components/graph/display";
import { CyElement } from "../base";

const props = defineProps<{
  artifact: ArtifactSchema;
  hidden?: boolean;
  faded?: boolean;
}>();

const { darkMode } = useTheme();

const typeColor = computed(
  () => typeOptionsStore.getArtifactLevel(props.artifact.type)?.color || ""
);

const definition = computed<ArtifactCytoElement>(() => {
  const { id, body, summary, type, name, safetyCaseType, logicType } =
    props.artifact;
  const warnings = warningStore.artifactWarnings[id] || [];
  const hiddenChildren = subtreeStore.getHiddenChildren(id);
  const hiddenChildWarnings = warningStore.getArtifactWarnings(hiddenChildren);
  const hiddenChildDeltaStates =
    deltaStore.getArtifactDeltaStates(hiddenChildren);
  const artifactDeltaState = deltaStore.getArtifactDeltaType(id);
  const isSelected = selectionStore.isArtifactInSelected(id);
  const opacity = props.hidden ? 0 : props.faded ? 0.3 : 1;

  return {
    data: {
      type: GraphElementType.node,
      graph: GraphMode.tree,
      id,

      body: summary || body,
      isCode: !summary && isCodeArtifact(name),
      artifactName: name,
      warnings,
      artifactType: type,
      artifactDeltaState,
      isSelected,
      opacity,
      typeColor: typeColor.value,
      hiddenChildren: hiddenChildren.length,
      childWarnings: hiddenChildWarnings,
      childDeltaStates: hiddenChildDeltaStates,
      safetyCaseType,
      logicType,
      dark: darkMode.value,
    },
  };
});
</script>
