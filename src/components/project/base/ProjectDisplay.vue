<template>
  <panel-card :title="project.name">
    <template #title-actions>
      <text-button
        v-if="editMode"
        text
        label="Cancel"
        icon="cancel"
        @click="appStore.closePanel(PanelType.projectEditor)"
      />
    </template>

    <div v-if="!editMode">
      <typography variant="caption" :value="versionLabel" />
      <br />
      <typography
        ep="p"
        variant="expandable"
        :value="description"
        default-expanded
      />
      <div class="q-mt-md">
        <flex-box wrap b="2">
          <div class="q-mb-sm">
            <attribute-chip :value="artifactLabel" icon="artifact" />
          </div>
          <div class="q-mb-sm">
            <attribute-chip :value="traceLabel" icon="trace" />
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
            <attribute-chip artifact-type :value="direction[1]" />
          </flex-box>
        </flex-box>
      </div>
    </div>
    <save-project-inputs
      v-else
      @save="appStore.closePanel(PanelType.projectEditor)"
    />
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
import { PanelType } from "@/types";
import { versionToString } from "@/util";
import { appStore, projectStore, timStore } from "@/hooks";
import {
  PanelCard,
  AttributeChip,
  Typography,
  FlexBox,
  Icon,
  TextButton,
} from "@/components/common";
import SaveProjectInputs from "./SaveProjectInputs.vue";

const editMode = computed(() => appStore.isProjectEditorOpen);

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
  timStore.traceMatrices.map((matrix) => [matrix.sourceType, matrix.targetType])
);
</script>
