<template>
  <cy-element3 :definition="definition" />
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
import { isCodeArtifact, sanitizeNodeId } from "@/util";
import {
  useTheme,
  deltaStore,
  selectionStore,
  subtreeStore,
  warningStore,
  typeOptionsStore,
} from "@/hooks";
import { CyElement3 } from "../base";

const props = defineProps<{
  artifact: ArtifactSchema;
  hidden?: boolean;
  faded?: boolean;
}>();

const { darkMode } = useTheme();

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
  const typeColor = typeOptionsStore.getArtifactLevel(type)?.color || "";

  return {
    data: {
      type: GraphElementType.node,
      graph: GraphMode.tree,
      id: sanitizeNodeId(id),
      body: summary || body,
      isCode: !summary && isCodeArtifact(name),
      artifactName: name,
      warnings,
      artifactType: type,
      artifactDeltaState,
      isSelected,
      opacity,
      typeColor,
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
