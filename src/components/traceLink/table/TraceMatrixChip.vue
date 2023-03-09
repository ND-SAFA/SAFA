<template>
  <div>
    <div v-if="doDisplay" @click.stop>
      <chip
        clickable
        outline
        :color="color"
        :style="style"
        @click="handleClick"
      >
        <typography :value="source.name" color="text" />
        <icon
          size="sm"
          class="q-mx-xs"
          :rotate="isChild ? -180 : 0"
          variant="trace"
        />
        <typography color="text" :value="target.name" />
      </chip>
    </div>
    <div v-else class="show-on-hover">
      <div class="width-fit" @click.stop>
        <icon-button
          icon="add"
          tooltip="Create trace link"
          @click="handleCreateLink"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
/**
 * Renders a chip representing a trace link between two artifacts.
 */
export default {
  name: "TraceMatrixChip",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ApprovalType, ArtifactSchema, TraceType } from "@/types";
import { appStore, selectionStore, subtreeStore, traceStore } from "@/hooks";
import { Typography, IconButton, Icon, Chip } from "@/components/common";

const props = defineProps<{
  source: ArtifactSchema;
  target: ArtifactSchema;
}>();

const direction = computed(() =>
  subtreeStore.getRelationship(props.source.id, props.target.id)
);

const isChild = computed(() => direction.value === "child");
const doDisplay = computed(() => !!direction.value);

const traceLink = computed(() =>
  isChild.value
    ? traceStore.getTraceLinkByArtifacts(props.target.id, props.source.id)
    : traceStore.getTraceLinkByArtifacts(props.source.id, props.target.id)
);

const isGenerated = computed(
  () => traceLink.value?.traceType === TraceType.GENERATED
);

const isUnreviewed = computed(
  () =>
    isGenerated.value &&
    traceLink.value?.approvalStatus === ApprovalType.UNREVIEWED
);

// Ignored until final decision is made on coloring logic.
// const color = computed(() =>
//   isGenerated.value
//     ? isUnreviewed.value
//       ? "secondary"
//       : "positive"
//     : "primary"
// );

const color = computed(() => (isGenerated.value ? "secondary" : "primary"));
const style = computed(
  () =>
    "border-width: 2px; " +
    (isUnreviewed.value ? "border-style: dashed;" : "border-style: solid;")
);

/**
 * Selects the trace link represented by this chip.
 */
function handleClick(): void {
  console.log({ traceLink });
  if (!traceLink.value) return;

  selectionStore.selectTraceLink(traceLink.value);
}

/**
 * Opens the trace creation panel to create a link between these artifacts.
 */
function handleCreateLink(): void {
  appStore.openTraceCreatorTo({
    type: "both",
    sourceId: props.source.id,
    targetId: props.target.id,
  });
}
</script>
