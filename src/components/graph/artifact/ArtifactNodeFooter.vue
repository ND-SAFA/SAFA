<template>
  <node-display
    v-if="showHiddenChildren"
    :color="props.color"
    variant="footer"
    :selected="props.selected"
    @click="viewsStore.extendDocumentSubtree(props.artifact)"
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
</template>

<script lang="ts">
/**
 * Renders the footer of an artifact node in the graph, when child artifacts are hidden.
 */
export default {
  name: "ArtifactNodeFooter",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactNodeDisplayProps } from "@/types";
import { getEnumColor } from "@/util";
import { deltaStore, viewsStore } from "@/hooks";
import { NodeDisplay } from "@/components/graph/display";
import { FlexBox, Icon, Typography, Separator } from "@/components/common";

const props = defineProps<Omit<ArtifactNodeDisplayProps, "deltaColor">>();

const hiddenChildrenLabel = computed(() =>
  props.hiddenChildren.length === 1
    ? "1 Hidden"
    : `${props.hiddenChildren.length} Hidden`
);
const showHiddenChildren = computed(() => props.hiddenChildren.length > 0);

const hiddenChildDeltaStates = computed(() =>
  deltaStore.getArtifactDeltaStates(props.hiddenChildren)
);
const showDelta = computed(() => deltaStore.inDeltaView);
const deltaClassName = computed(() =>
  showDelta.value && props.hiddenChildren.length > 0
    ? "cy-node-delta-footer"
    : ""
);
const childDeltaColors = computed(() =>
  hiddenChildDeltaStates.value.map(getEnumColor)
);
</script>
