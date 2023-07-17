<template>
  <div>
    <panel-card>
      <artifact-body-display
        v-if="targetArtifact"
        :artifact="targetArtifact"
        display-title
        display-divider
        default-expanded
        data-cy="panel-trace-link-target"
      />
      <template #actions>
        <text-button
          text
          label="View Artifact"
          data-cy="button-trace-target"
          icon="artifact"
          @click="handleViewTarget"
        />
      </template>
    </panel-card>
    <flex-box justify="center" align="center" b="4">
      <icon size="md" :rotate="270" variant="trace" color="primary" />
      <attribute-chip v-if="!!score" confidence-score :value="score" />
    </flex-box>
    <panel-card>
      <artifact-body-display
        v-if="sourceArtifact"
        :artifact="sourceArtifact"
        display-title
        display-divider
        default-expanded
        data-cy="panel-trace-link-source"
      />
      <template #actions>
        <text-button
          text
          label="View Artifact"
          data-cy="button-trace-source"
          icon="artifact"
          @click="handleViewSource"
        />
      </template>
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
import {
  ArtifactBodyDisplay,
  FlexBox,
  AttributeChip,
  PanelCard,
  TextButton,
  Icon,
} from "@/components/common";

const traceLink = computed(() => selectionStore.selectedTraceLink);

const sourceArtifact = computed(() =>
  artifactStore.getArtifactById(traceLink.value?.sourceId || "")
);
const targetArtifact = computed(() =>
  artifactStore.getArtifactById(traceLink.value?.targetId || "")
);

const score = computed(() =>
  traceLink.value?.traceType === TraceType.GENERATED
    ? String(traceLink.value.score)
    : ""
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
