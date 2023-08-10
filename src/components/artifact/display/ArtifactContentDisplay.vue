<template>
  <flex-box full-width :column="!isCode">
    <div style="min-width: 400px">
      <typography
        variant="caption"
        :value="showSummary ? 'Summary' : 'Content'"
      />
      <artifact-body-display
        :artifact="props.artifact"
        default-expanded
        :full-width="!showSummary"
      />
    </div>
    <div v-if="showSummary">
      <typography variant="caption" value="Content" />
      <typography
        :variant="isCode ? 'code' : 'expandable'"
        :value="props.artifact.body"
        l="3"
      />
    </div>
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays both the body and summary of an artifact.
 * If no summary exists, only the artifact body is displayed.
 */
export default {
  name: "ArtifactContentDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactSchema } from "@/types";
import { FlexBox, Typography } from "@/components/common";
import ArtifactBodyDisplay from "./ArtifactBodyDisplay.vue";

const props = defineProps<{
  /**
   * The artifact to display.
   */
  artifact: ArtifactSchema;
}>();

const showSummary = computed(() => !!props.artifact.summary);
const isCode = computed(() => props.artifact.isCode);
</script>
