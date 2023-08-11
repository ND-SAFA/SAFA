<template>
  <details-panel panel="displayTraceMatrix">
    <flex-box v-if="displayActions" b="2">
      <text-button
        text
        label="View Artifacts"
        icon="view-tree"
        @click="handleViewLevel"
      />
    </flex-box>

    <panel-card>
      <flex-box align="center" justify="between" class="overflow-hidden">
        <div class="overflow-hidden" data-cy="text-selected-name">
          <typography variant="caption" value="Parent Type" />
          <typography
            ellipsis
            variant="subtitle"
            el="h1"
            class="q-my-none"
            :value="targetType"
          />
          <typography variant="caption" value="Child Type" />
          <typography
            ellipsis
            variant="subtitle"
            el="h1"
            class="q-my-none"
            :value="sourceType"
          />
          <q-tooltip>{{ name }}</q-tooltip>
        </div>
        <flex-box column>
          <icon :id="targetIcon" size="sm" :color="targetColor" />
          <icon
            class="q-my-xs"
            size="sm"
            :color="generatedCount > 0 ? 'nodeGenerated' : 'nodeDefault'"
            variant="trace"
            :rotate="-90"
          />
          <icon :id="sourceIcon" size="sm" :color="sourceColor" />
        </flex-box>
      </flex-box>

      <separator b="2" t="1" />

      <typography variant="caption" value="Total Trace Links" />
      <typography el="p" :value="totalCount" />
      <typography variant="caption" value="Generated Trace Links" />
      <typography el="p" :value="generatedCount" />
      <typography variant="caption" value="Approved Trace Links" />
      <typography el="p" :value="approvedCount" />
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays trace matrix information.
 */
export default {
  name: "TraceMatrixPanel",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  documentStore,
  projectStore,
  selectionStore,
  sessionStore,
  timStore,
} from "@/hooks";
import {
  PanelCard,
  Typography,
  TextButton,
  Icon,
  DetailsPanel,
  FlexBox,
  Separator,
} from "@/components/common";

const displayActions = computed(() =>
  sessionStore.isEditor(projectStore.project)
);

const traceMatrix = computed(() => selectionStore.selectedTraceMatrix);

const sourceType = computed(() => traceMatrix.value?.sourceType || "");
const sourceIcon = computed(() => timStore.getTypeIcon(sourceType.value));
const sourceColor = computed(() => timStore.getTypeColor(sourceType.value));

const targetType = computed(() => traceMatrix.value?.targetType || "");
const targetIcon = computed(() => timStore.getTypeIcon(targetType.value));
const targetColor = computed(() => timStore.getTypeColor(targetType.value));

const name = computed(() => `"${sourceType.value}" to "${targetType.value}"`);

const totalCount = computed(() => {
  const count = traceMatrix.value?.count || 0;

  return count === 1 ? "1 Link" : `${count} Links`;
});

const generatedCount = computed(() => {
  const count = traceMatrix.value?.generatedCount || 0;

  return count === 1 ? "1 Link" : `${count} Links`;
});

const approvedCount = computed(() => {
  const count = traceMatrix.value?.approvedCount || 0;

  return count === 1 ? "1 Link" : `${count} Links`;
});

/**
 * Switches to tree view and highlights this type matrix.
 */
function handleViewLevel(): void {
  if (!traceMatrix.value) return;

  documentStore.addDocumentOfTypes([
    traceMatrix.value.sourceType,
    traceMatrix.value.targetType,
  ]);
}
</script>
