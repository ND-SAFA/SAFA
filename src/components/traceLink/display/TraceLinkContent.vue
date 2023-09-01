<template>
  <div>
    <panel-card :title="title">
      <template #title-actions>
        <attribute-chip v-if="!!score" confidence-score :value="score" />
      </template>

      <div v-if="!!explanation">
        <typography variant="caption" value="Explanation" />
        <typography
          :value="explanation"
          variant="expandable"
          default-expanded
        />
      </div>

      <typography variant="caption" value="Parent" />
      <artifact-body-display
        v-if="targetArtifact"
        :artifact="targetArtifact"
        display-title
        default-expanded
        clickable
        data-cy="panel-trace-link-target"
        @click="handleViewTarget"
      />

      <typography variant="caption" value="Child" />
      <artifact-body-display
        v-if="sourceArtifact"
        :artifact="sourceArtifact"
        display-title
        default-expanded
        clickable
        data-cy="panel-trace-link-source"
        @click="handleViewSource"
      />
    </panel-card>
  </div>
</template>

<script lang="ts">
/**
 * Displays trace link information.
 */
export default {
  name: "TraceLinkContent",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { TraceType } from "@/types";
import { artifactStore, selectionStore } from "@/hooks";
import { AttributeChip, PanelCard, Typography } from "@/components/common";
import { ArtifactBodyDisplay } from "@/components/artifact/display";

const traceLink = computed(() => selectionStore.selectedTraceLink);

const sourceArtifact = computed(() =>
  artifactStore.getArtifactById(traceLink.value?.sourceId || "")
);
const targetArtifact = computed(() =>
  artifactStore.getArtifactById(traceLink.value?.targetId || "")
);

const generated = computed(
  () => traceLink.value?.traceType === TraceType.GENERATED
);

const score = computed(() =>
  generated.value ? String(traceLink.value?.score) : ""
);

const title = computed(() =>
  generated.value ? "Generated Link" : "Manual Link"
);

const explanation = computed(() =>
  generated.value ? traceLink.value?.explanation : undefined
);

/**
 * Views the target artifact.
 */
function handleViewTarget(): void {
  selectionStore.selectArtifact(traceLink.value?.targetId || "");
}

/**
 * Views the source artifact.
 */
function handleViewSource(): void {
  selectionStore.selectArtifact(traceLink.value?.sourceId || "");
}
</script>
