<template>
  <div>
    <div v-if="!!explanation">
      <typography variant="caption" value="Explanation" />
      <typography
        :value="explanation"
        variant="expandable"
        default-expanded
        :collapse-length="0"
      />
    </div>

    <q-splitter v-if="!showOnly" v-model="splitterModel">
      <template #before>
        <artifact-body-display
          v-if="sourceArtifact"
          :artifact="sourceArtifact"
          display-title
          display-divider
          default-expanded
        />
      </template>
      <template #after>
        <artifact-body-display
          v-if="targetArtifact"
          :artifact="targetArtifact"
          display-title
          display-divider
          default-expanded
        />
      </template>
    </q-splitter>

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
import { computed, ref } from "vue";
import { TraceLinkDisplayProps } from "@/types";
import { artifactStore } from "@/hooks";
import { Typography } from "@/components/common";
import {
  ArtifactContentDisplay,
  ArtifactBodyDisplay,
} from "@/components/artifact/display";

const props = defineProps<TraceLinkDisplayProps>();

const splitterModel = ref(50);

const sourceArtifact = computed(() =>
  artifactStore.getArtifactById(props.trace.sourceId)
);
const targetArtifact = computed(() =>
  artifactStore.getArtifactById(props.trace.targetId)
);

const showOnlyArtifact = computed(() =>
  props.showOnly === "source" ? sourceArtifact.value : targetArtifact.value
);

const generated = computed(() => props.trace.traceType === "GENERATED");
const explanation = computed(() =>
  generated.value ? props.trace.explanation : undefined
);
</script>
