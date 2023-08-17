<template>
  <node-display
    v-if="props.selected"
    :color="props.color"
    variant="sidebar"
    :selected="props.selected"
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
        data-cy="button-toggle-subtree"
        @click="subtreeStore.showSubtree(id)"
      />
      <icon-button
        v-else-if="hasSubtree"
        tooltip="Hide subtree"
        icon="group-close-all"
        data-cy="button-toggle-subtree"
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
</template>

<script lang="ts">
/**
 * Renders actions for the selected artifact node.
 */
export default {
  name: "ArtifactNodeActions",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactNodeDisplayProps } from "@/types";
import {
  subtreeStore,
  documentStore,
  appStore,
  permissionStore,
} from "@/hooks";
import { NodeDisplay } from "@/components/graph/display";
import { FlexBox, Separator, IconButton } from "@/components/common";

const props = defineProps<Omit<ArtifactNodeDisplayProps, "deltaColor">>();

const displayEditing = computed(() => permissionStore.projectAllows("editor"));

const id = computed(() => props.artifact.id);

const hasSubtree = computed(
  () => subtreeStore.getChildren(id.value).length > 0
);
const showHiddenChildren = computed(() => props.hiddenChildren.length > 0);
</script>
