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
import { computed, defineProps } from "vue";
import { useTheme } from "vuetify";
import { ArtifactSchema, GraphElementType, GraphMode } from "@/types";
import {
  deltaStore,
  selectionStore,
  subtreeStore,
  warningStore,
} from "@/hooks";
import { CyElement3 } from "../base";

const props = defineProps<{
  artifact: ArtifactSchema;
  hidden?: boolean;
  faded?: boolean;
}>();

const theme = useTheme();
const darkMode = computed(() => theme.global.current.value.dark);

const definition = computed(() => {
  const { id, body, type, name, safetyCaseType, logicType } = props.artifact;
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
      body,
      artifactName: name,
      warnings,
      artifactType: type,
      artifactDeltaState,
      isSelected,
      opacity,
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
