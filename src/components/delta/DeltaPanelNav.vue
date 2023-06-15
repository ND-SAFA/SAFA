<template>
  <panel-card>
    <text-button
      v-if="version && !!version.versionId"
      block
      outlined
      label="Hide Delta View"
      icon="cancel"
      class="q-mb-md"
      @click="handleClose"
    />
    <select-input
      v-model="version"
      :options="versions"
      :loading="loading"
      option-value="versionId"
      :option-label="getVersionName"
      label="Delta Version"
      hint="The version to view the delta between."
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
import { deltaStore, projectStore, setProjectApiStore } from "@/hooks";
import { getProjectVersions, handleSetProjectDelta } from "@/api";
import { TextButton, PanelCard, SelectInput } from "@/components/common";

const loading = ref(false);
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
 * Disables delta view.
 */
function handleClose(): void {
  setProjectApiStore.handleReloadProject();
}

onMounted(() => loadVersions());
</script>
