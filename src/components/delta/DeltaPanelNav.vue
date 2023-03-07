<template>
  <panel-card>
    <text-button
      v-if="!selectorVisible"
      block
      label="Compare Versions"
      color="primary"
      icon="view-delta"
      @click="handleChange"
    />
    <text-button
      v-else
      block
      outlined
      label="Hide Delta View"
      icon="cancel"
      @click="handleChange"
    />
    <select-input
      v-model="version"
      :disabled="!selectorVisible"
      :options="versions"
      :loading="loading"
      option-value="versionId"
      :option-label="getVersionName"
      label="Delta Version"
      class="q-mt-md"
    />
  </panel-card>
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
import { ref, onMounted, computed } from "vue";
import { VersionSchema } from "@/types";
import { versionToString } from "@/util";
import { deltaStore, projectStore } from "@/hooks";
import {
  getProjectVersions,
  handleReloadProject,
  handleSetProjectDelta,
} from "@/api";
import { TextButton, PanelCard, SelectInput } from "@/components/common";

const loading = ref(false);
const selectorVisible = ref(deltaStore.inDeltaView);
const versions = ref<VersionSchema[]>([]);

const version = computed({
  get() {
    return deltaStore.afterVersion;
  },
  set(newVersion) {
    if (!newVersion || !projectStore.version) return;

    loading.value = true;

    handleSetProjectDelta(projectStore.version, newVersion, () => {
      loading.value = false;
    });
  },
});

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
  if (selectorVisible.value) {
    deltaStore.setIsDeltaViewEnabled(false);
    handleReloadProject();
    selectorVisible.value = false;
  } else {
    selectorVisible.value = true;
  }
}

onMounted(() => loadVersions());
</script>
