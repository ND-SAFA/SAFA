<template>
  <cy-element
    :definition="definition"
    :style="style"
    :data-cy="dataCy"
    :data-cy-name="props.artifact.name"
  >
    <node-display
      separator
      :color="color"
      variant="artifact"
      :title="props.artifact.type"
      :subtitle="displayName"
    >
      <separator
        v-if="showDelta"
        :color="deltaColor"
        class="cy-node-delta-chip"
      />
    </node-display>

    <node-display
      v-if="hiddenChildren.length > 0"
      :color="color"
      variant="footer"
      @click.stop="subtreeStore.showSubtree(props.artifact.id)"
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
import { getEnumColor, isCodeArtifact } from "@/util";
import {
  useTheme,
  deltaStore,
  selectionStore,
  subtreeStore,
  warningStore,
  typeOptionsStore,
} from "@/hooks";
import { NodeDisplay } from "@/components/graph/display";
import { FlexBox, Icon, Typography, Separator } from "@/components/common";
import { CyElement } from "../base";

const props = defineProps<{
  artifact: ArtifactSchema;
  hidden?: boolean;
  faded?: boolean;
}>();

const { darkMode } = useTheme();

const opacity = computed(() => (props.hidden ? 0 : props.faded ? 0.3 : 1));
const style = computed(() => `opacity: ${opacity.value};`);

const displayName = computed(
  () =>
    (isCodeArtifact(props.artifact.name) &&
      props.artifact.name.split("/").pop()) ||
    props.artifact.name
);

const hiddenChildren = computed(() =>
  subtreeStore.getHiddenChildren(props.artifact.id)
);
const hiddenChildrenLabel = computed(() =>
  hiddenChildren.value.length === 1
    ? "1 Hidden"
    : `${hiddenChildren.value.length} Hidden`
);

const deltaState = computed(() =>
  deltaStore.getArtifactDeltaType(props.artifact.id)
);
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

const typeColor = computed(
  () => typeOptionsStore.getArtifactLevel(props.artifact.type)?.color || ""
);
const color = computed(() =>
  showDelta.value ? deltaColor.value : typeColor.value
);

const selected = computed(() =>
  selectionStore.isArtifactInSelected(props.artifact.id)
);

const dataCy = computed(() =>
  selected.value ? "tree-node-selected" : "tree-node"
);

const definition = computed<ArtifactCytoElement>(() => {
  const { id, body, summary, type, name, safetyCaseType, logicType } =
    props.artifact;
  const warnings = warningStore.artifactWarnings[id] || [];
  const hiddenChildWarnings = warningStore.getArtifactWarnings(
    hiddenChildren.value
  );

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
      artifactDeltaState: deltaState.value,
      isSelected: selected.value,
      opacity: opacity.value,
      typeColor: typeColor.value,
      hiddenChildren: hiddenChildren.value.length,
      childWarnings: hiddenChildWarnings,
      childDeltaStates: hiddenChildDeltaStates.value,
      safetyCaseType,
      logicType,
      dark: darkMode.value,
    },
  };
});
</script>
