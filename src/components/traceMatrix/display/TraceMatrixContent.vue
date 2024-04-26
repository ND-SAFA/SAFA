<template>
  <panel-card borderless>
    <template #title>
      <div class="overflow-hidden" data-cy="text-selected-name">
        <typography variant="caption" value="Parent" />
        <list-item
          clickable
          @click="selectionStore.selectArtifactLevel(targetType)"
        >
          <typography
            ellipsis
            variant="subtitle"
            el="h1"
            class="q-my-none"
            :value="targetType"
          />
          <q-tooltip>{{ targetType }}</q-tooltip>
        </list-item>
        <typography variant="caption" value="Child" />
        <list-item
          clickable
          @click="selectionStore.selectArtifactLevel(sourceType)"
        >
          <typography
            ellipsis
            variant="subtitle"
            el="h1"
            class="q-my-none"
            :value="sourceType"
          />
          <q-tooltip>{{ sourceType }}</q-tooltip>
        </list-item>
      </div>
    </template>

    <template #title-actions>
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
    </template>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays attributes of the selected trace matrix.
 */
export default {
  name: "TraceMatrixContent",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { selectionStore, timStore } from "@/hooks";
import {
  PanelCard,
  Typography,
  Icon,
  FlexBox,
  ListItem,
} from "@/components/common";

const traceMatrix = computed(() => timStore.selectedTraceMatrix);
const generatedCount = computed(() => traceMatrix.value?.generatedCount || 0);

const sourceType = computed(() => traceMatrix.value?.sourceType || "");
const sourceIcon = computed(() => timStore.getTypeIcon(sourceType.value));
const sourceColor = computed(() => timStore.getTypeColor(sourceType.value));

const targetType = computed(() => traceMatrix.value?.targetType || "");
const targetIcon = computed(() => timStore.getTypeIcon(targetType.value));
const targetColor = computed(() => timStore.getTypeColor(targetType.value));
</script>
