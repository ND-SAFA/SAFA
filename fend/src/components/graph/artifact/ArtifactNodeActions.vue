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
        @click="viewsStore.addDocumentOfNeighborhood(props.artifact)"
      />
      <icon-button
        v-if="showHiddenChildren && hasSubtree"
        tooltip="Show subtree"
        icon="group-open-all"
        data-cy="button-toggle-subtree"
        @click="viewsStore.extendDocumentSubtree(props.artifact)"
      />
      <icon-button
        v-else-if="hasSubtree"
        tooltip="Hide subtree"
        icon="group-close-all"
        data-cy="button-toggle-subtree"
        @click="subtreeStore.hideSubtree(id)"
      />

      <separator v-if="displayActions" class="full-width q-my-xs" />

      <icon-button
        v-if="displayActions"
        tooltip="Add parent"
        icon="trace"
        :rotate="-90"
        :color="props.color"
        @click="
          traceSaveStore.openPanel({
            type: 'source',
            artifactId: id,
          })
        "
      />
      <icon-button
        v-if="displayActions"
        tooltip="Add child"
        icon="trace"
        :rotate="90"
        :color="props.color"
        @click="
          traceSaveStore.openPanel({
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
  permissionStore,
  traceSaveStore,
  viewsStore,
} from "@/hooks";
import { NodeDisplay } from "@/components/graph/display";
import { FlexBox, Separator, IconButton } from "@/components/common";

const props = defineProps<Omit<ArtifactNodeDisplayProps, "deltaColor">>();

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);

const id = computed(() => props.artifact.id);

const hasSubtree = computed(
  () => subtreeStore.getChildren(id.value).length > 0
);
const showHiddenChildren = computed(() => props.hiddenChildren.length > 0);
</script>
