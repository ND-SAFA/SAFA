<template>
  <q-select
    v-if="isProjectDefined"
    v-model="version"
    outlined
    dark
    :options-dark="darkMode"
    options-selected-class="primary"
    label="Version"
    :options="versions"
    option-value="versionId"
    class="nav-input nav-version q-ml-sm"
    color="accent"
  >
    <template #selected>
      {{ versionToString(version) }}
    </template>
    <template #option="{ opt, itemProps }">
      <list-item v-bind="itemProps" :title="versionToString(opt)" />
    </template>
    <template #after-options>
      <text-button
        text
        label="Add Version"
        icon="add"
        @click="openCreateVersion = true"
      />
    </template>
    <template #after>
      <version-creator
        :open="openCreateVersion"
        :project="project"
        @close="openCreateVersion = false"
        @create="handleVersionCreated"
      />
    </template>
  </q-select>
</template>

<script lang="ts">
/**
 * Displays the current project version, and allows it to be changed.
 */
export default {
  name: "VersionSelector",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { VersionSchema } from "@/types";
import { versionToString } from "@/util";
import { projectStore, useTheme } from "@/hooks";
import { getProjectVersions, handleLoadVersion } from "@/api";
import { TextButton, ListItem } from "@/components/common";
import VersionCreator from "./VersionCreator.vue";

const versions = ref<VersionSchema[]>([]);
const openCreateVersion = ref(false);

const { darkMode } = useTheme();

const project = computed(() => projectStore.project);
const isProjectDefined = computed(() => projectStore.isProjectDefined);

const version = computed({
  get: () => projectStore.version,
  set(version: VersionSchema | undefined) {
    if (!version) return;

    handleLoadVersion(version.versionId);
  },
});

/**
 * Loads the versions of the current project.
 */
async function updateVersionList(): Promise<void> {
  const { projectId } = project.value;
  versions.value = projectId ? await getProjectVersions(projectId) : [];
}

/**
 * Adds the new version the version list and loads that version.
 * @param version - The new version.
 */
async function handleVersionCreated(version: VersionSchema): Promise<void> {
  versions.value = [version, ...versions.value];
  openCreateVersion.value = false;
  await handleLoadVersion(version.versionId);
}

onMounted(() => updateVersionList());

watch(
  () => project.value,
  () => updateVersionList()
);
</script>
