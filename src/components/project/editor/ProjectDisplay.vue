<template>
  <panel-card :title="name">
    <template #title-actions>
      <text-button
        v-if="editMode"
        text
        label="Cancel"
        icon="cancel"
        @click="appStore.close('editProject')"
      />
      <typography v-else secondary :value="versionLabel" />
    </template>

    <div v-if="!editMode">
      <flex-box column b="4">
        <typography value="Project Data" variant="caption" />

        <typography :value="artifactTypeLabel" />
        <typography :value="artifactLabel" />
        <typography :value="traceLabel" />
      </flex-box>

      <typography value="Artifact Types" variant="caption" />
      <flex-box
        v-for="[parent, children] in artifactTypeMap"
        :key="parent"
        column
        t="3"
      >
        <attribute-chip artifact-type :value="parent" />
        <flex-box v-if="children.length > 0" l="4">
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
    </div>

    <save-project-inputs v-else @save="appStore.close('editProject')" />
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
import {
  appStore,
  artifactStore,
  projectStore,
  timStore,
  traceStore,
} from "@/hooks";
import {
  PanelCard,
  AttributeChip,
  FlexBox,
  Icon,
  TextButton,
  Typography,
} from "@/components/common";
import SaveProjectInputs from "./SaveProjectInputs.vue";

const editMode = computed(() => appStore.popups.editProject);

const project = computed(() => projectStore.project);

const name = computed(() => projectStore.project.name || "No Project");

const versionLabel = computed(
  () => `Version ${versionToString(project.value.projectVersion)}`
);

const artifactTypeLabel = computed(
  () => `${timStore.artifactTypes.length} Artifact Types`
);

const artifactLabel = computed(
  () => `${artifactStore.allArtifacts.length} Artifacts`
);

const traceLabel = computed(() => `${traceStore.allTraces.length} Trace Links`);

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
      timStore.artifactTypes
        .map(({ name }) => ({ [name]: [] }))
        .reduce(
          (acc, cur) => ({ ...acc, ...cur }),
          {} as Record<string, string[]>
        )
    )
  )
);
</script>
