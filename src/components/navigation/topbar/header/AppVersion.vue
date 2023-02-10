<template>
  <flex-box align="center">
    <typography
      el="h1"
      variant="subtitle"
      color="white"
      style="white-space: nowrap"
      :value="projectName"
      x="4"
    />
    <v-select
      v-if="isProjectDefined"
      outlined
      hide-details
      dark
      dense
      label="Version"
      :value="version"
      :items="versions"
      item-value="versionId"
      style="width: 100px"
      class="nav-input"
      @input="handleLoadVersion"
    >
      <template #selection>
        {{ versionToString(version) }}
      </template>
      <template #item="{ item }">
        {{ versionToString(item) }}
      </template>
      <template #append-item>
        <text-button text variant="add" @click="openCreateVersion = true">
          Add Version
        </text-button>
      </template>
    </v-select>

    <version-creator
      :is-open="openCreateVersion"
      :project="project"
      @close="openCreateVersion = false"
      @create="handleVersionCreated"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays the current project version.
 */
export default {
  name: "AppVersion",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { VersionSchema } from "@/types";
import { versionToString } from "@/util";
import { projectStore } from "@/hooks";
import { getProjectVersions, handleLoadVersion } from "@/api";
import { Typography, FlexBox, TextButton } from "@/components/common";
import { VersionCreator } from "@/components/project/selector";

const versions = ref<VersionSchema[]>([]);
const openCreateVersion = ref(false);

const project = computed(() => projectStore.project);
const version = computed(() => projectStore.version);
const isProjectDefined = computed(() => projectStore.isProjectDefined);
const projectName = computed(() =>
  isProjectDefined.value ? project.value.name : "No Project Selected"
);

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
