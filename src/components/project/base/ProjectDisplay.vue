<template>
  <panel-card :title="project.name">
    <typography variant="caption" :value="versionLabel" />
    <br />
    <typography ep="p" :value="description" />
    <div class="q-mt-md">
      <flex-box wrap b="2">
        <div class="q-mb-sm">
          <attribute-chip
            :value="artifactLabel"
            icon="artifact"
            color="primary"
          />
        </div>
        <div class="q-mb-sm">
          <attribute-chip :value="traceLabel" icon="trace" color="primary" />
        </div>
      </flex-box>
      <flex-box
        v-for="direction in typeDirections"
        :key="direction[0]"
        wrap
        b="2"
        align="center"
      >
        <attribute-chip artifact-type :value="direction[0]" />
        <flex-box wrap>
          <icon
            class="q-mx-xs q-mt-xs"
            size="sm"
            color="primary"
            variant="trace"
          />
          <div v-for="type in direction[1]" :key="type">
            <attribute-chip artifact-type :value="type" />
          </div>
        </flex-box>
      </flex-box>
    </div>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays high level project information.
 */
export default {
  name: "ProjectDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { versionToString } from "@/util";
import { projectStore, typeOptionsStore } from "@/hooks";
import {
  PanelCard,
  AttributeChip,
  Typography,
  FlexBox,
  Icon,
} from "@/components/common";

const project = computed(() => projectStore.project);

const versionLabel = computed(
  () => `Version ${versionToString(project.value.projectVersion)}`
);

const artifactLabel = computed(
  () => `${project.value.artifacts.length} Artifacts`
);

const traceLabel = computed(() => `${project.value.traces.length} Trace Links`);

const description = computed(
  () => project.value.description || "No Description."
);

const typeDirections = computed(() =>
  Object.values(typeOptionsStore.artifactLevels)
    .map((level) => [level.name, level.allowedTypes] as [string, string[]])
    .filter(([, targets]) => targets.length > 0)
);
</script>
