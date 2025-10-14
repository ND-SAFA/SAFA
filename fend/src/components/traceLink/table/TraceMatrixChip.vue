<template>
  <div>
    <div v-if="doDisplay" @click.stop>
      <chip clickable outlined :class="className" @click="handleClick">
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
          small
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
import { TraceMatrixChipProps } from "@/types";
import {
  selectionStore,
  subtreeStore,
  traceSaveStore,
  traceStore,
} from "@/hooks";
import { Typography, IconButton, Icon, Chip } from "@/components/common";

const props = defineProps<TraceMatrixChipProps>();

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

const isGenerated = computed(() => traceLink.value?.traceType === "GENERATED");

const isUnreviewed = computed(
  () => isGenerated.value && traceLink.value?.approvalStatus === "UNREVIEWED"
);

const className = computed(() => {
  const base = isGenerated.value
    ? "trace-chip-generated text-nodeGenerated "
    : "trace-chip text-nodeDefault ";
  const unreviewed = isUnreviewed.value ? "trace-chip-unreviewed" : "";

  return base + unreviewed;
});

/**
 * Selects the trace link represented by this chip.
 */
function handleClick(): void {
  if (!traceLink.value) return;

  selectionStore.selectTraceLink(traceLink.value);
}

/**
 * Opens the trace creation panel to create a link between these artifacts.
 */
function handleCreateLink(): void {
  traceSaveStore.openPanel({
    type: "both",
    sourceIds: [props.source.id],
    targetIds: [props.target.id],
  });
}
</script>
