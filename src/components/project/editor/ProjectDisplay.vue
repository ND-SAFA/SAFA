<template>
  <panel-card :title="project.name">
    <template #title-actions>
      <text-button
        v-if="editMode"
        text
        label="Cancel"
        icon="cancel"
        @click="appStore.close('editProject')"
      />
    </template>

    <div v-if="!editMode">
      <flex-box full-width justify="between">
        <attribute-chip :value="versionLabel" />
        <div>
          <attribute-chip :value="artifactLabel" icon="artifact" />
          <attribute-chip :value="traceLabel" icon="trace" />
        </div>
      </flex-box>

      <typography variant="caption" value="Description" />
      <typography
        ep="p"
        variant="expandable"
        :value="description"
        default-expanded
      />

      <expansion-item label="Artifact Types">
        <flex-box
          v-for="[parent, children] in artifactTypeMap"
          :key="parent"
          column
          t="2"
        >
          <attribute-chip artifact-type :value="parent" />
          <flex-box l="4">
            <icon
              class="q-mx-xs q-mt-xs"
              size="sm"
              color="text"
              variant="trace"
              :rotate="-90"
            />
            <flex-box column>
              <attribute-chip
                v-for="child in children"
                :key="child"
                artifact-type
                :value="child"
              />
            </flex-box>
          </flex-box>
        </flex-box>
      </expansion-item>
    </div>

    <save-project-inputs v-else @click="appStore.close('editProject')" />
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
import { appStore, projectStore, timStore } from "@/hooks";
import {
  PanelCard,
  AttributeChip,
  Typography,
  FlexBox,
  Icon,
  TextButton,
  ExpansionItem,
} from "@/components/common";
import SaveProjectInputs from "./SaveProjectInputs.vue";

const editMode = computed(() => appStore.popups.editProject);

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

const artifactTypeMap = computed(() =>
  Object.entries(
    timStore.traceMatrices.reduce(
      (acc, matrix) => ({
        ...acc,
        [matrix.targetType]: [
          ...(acc[matrix.targetType] || []),
          matrix.sourceType,
        ],
      }),
      {} as Record<string, string[]>
    )
  )
);
</script>
