<template>
  <div>
    <flex-box v-if="!showOnly" full-width y="1" justify="between" :wrap="false">
      <artifact-body-display
        v-if="sourceArtifact"
        :artifact="sourceArtifact"
        display-title
        display-divider
        default-expanded
      />
      <separator vertical />
      <artifact-body-display
        v-if="targetArtifact"
        :artifact="targetArtifact"
        display-title
        display-divider
        default-expanded
      />
    </flex-box>

    <artifact-content-display
      v-else-if="showOnlyArtifact"
      :artifact="showOnlyArtifact"
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
  ArtifactBodyDisplay,
  ArtifactContentDisplay,
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

const showOnlyArtifact = computed(() =>
  props.showOnly === "source" ? sourceArtifact.value : targetArtifact.value
);
</script>
