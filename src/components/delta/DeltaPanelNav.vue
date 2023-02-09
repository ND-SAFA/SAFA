<template>
  <div class="mt-4">
    <text-button
      v-if="!isSelectorVisible"
      block
      large
      color="primary"
      icon-id="mdi-source-branch"
      @click="handleChange"
    >
      Compare Versions
    </text-button>
    <text-button
      v-else
      block
      large
      outlined
      variant="cancel"
      @click="handleChange"
    >
      Hide Delta View
    </text-button>

    <v-select
      v-if="isSelectorVisible"
      filled
      :model-value="deltaStore.afterVersion"
      :items="versions"
      :loading="isLoading"
      item-value="versionId"
      label="Delta Version"
      class="mt-4"
      @update:model-value="handleSetVersion"
    >
      <template #selection>
        {{ getVersionName(deltaStore.afterVersion) }}
      </template>
      <template #item="{ item }">
        {{ getVersionName(item) }}
      </template>
    </v-select>
  </div>
</template>

<script lang="ts">
/**
 * Displays the delta panel navigation.
 */
export default {
  name: "DeltaPanelNav",
};
</script>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { VersionSchema } from "@/types";
import { versionToString } from "@/util";
import { deltaStore, projectStore } from "@/hooks";
import {
  getProjectVersions,
  handleReloadProject,
  handleSetProjectDelta,
} from "@/api";
import { TextButton } from "@/components/common";

const isLoading = ref(false);
const isSelectorVisible = ref(deltaStore.inDeltaView);
const versions = ref<VersionSchema[]>([]);

/**
 * Loads a new version.
 * @param newVersionId - The version to load.
 */
function handleSetVersion(newVersionId: string): void {
  const newVersion = versions.value.find(
    ({ versionId }) => versionId === newVersionId
  );

  if (!newVersion || !projectStore.version) return;

  isLoading.value = true;

  handleSetProjectDelta(projectStore.version, newVersion, () => {
    isLoading.value = false;
  });
}

/**
 * Returns a version's name.
 * @param version - The version to name.
 * @return The version's name.
 */
function getVersionName(version: VersionSchema): string {
  return versionToString(version);
}

/**
 * Loads the versions of the current project.
 */
async function loadVersions(): Promise<void> {
  const projectId = projectStore.projectId;

  versions.value = projectId
    ? (await getProjectVersions(projectId)).filter(
        ({ versionId }) => versionId !== projectStore.version?.versionId
      )
    : [];
}

/**
 * Changes whether delta view is enabled.
 */
function handleChange(): void {
  if (isSelectorVisible.value) {
    deltaStore.setIsDeltaViewEnabled(false);
    handleReloadProject();
    isSelectorVisible.value = false;
  } else {
    isSelectorVisible.value = true;
  }
}

onMounted(() => loadVersions());
</script>
