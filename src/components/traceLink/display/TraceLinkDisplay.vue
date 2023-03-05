<template>
  <div>
    <flex-box v-if="!showOnly" full-width y="1" justify="between" :wrap="false">
      <artifact-body-display
        :artifact="sourceArtifact"
        display-title
        display-divider
      />
      <separator vertical />
      <artifact-body-display
        :artifact="targetArtifact"
        display-title
        display-divider
      />
    </flex-box>

    <typography
      v-else
      default-expanded
      t="1"
      variant="expandable"
      :value="
        showOnly === 'source' ? sourceArtifact?.body : targetArtifact?.body
      "
    />
  </div>
</template>

<script lang="ts">
/**
 * Displays a trace link's artifacts.
 */
export default {
  name: "TraceLinkDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { TraceLinkSchema } from "@/types";
import { artifactStore } from "@/hooks";
import {
  Typography,
  ArtifactBodyDisplay,
  FlexBox,
  Separator,
} from "@/components/common";

const props = defineProps<{
  /**
   * The trace link to display.
   */
  trace: TraceLinkSchema;
  /**
   * Whether to display only the source or target artifact.
   */
  showOnly?: "source" | "target";
}>();

const sourceArtifact = computed(() =>
  artifactStore.getArtifactById(props.trace.sourceId)
);
const targetArtifact = computed(() =>
  artifactStore.getArtifactById(props.trace.targetId)
);
</script>
