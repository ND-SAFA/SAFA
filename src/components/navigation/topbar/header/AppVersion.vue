<template>
  <flex-box align="center" r="1">
    <typography
      el="h1"
      variant="subtitle"
      color="white"
      style="white-space: nowrap"
      :value="projectName"
      x="4"
    />
    <q-select
      v-if="isProjectDefined"
      v-model="version"
      dense
      outlined
      dark
      :options-dark="false"
      label="Version"
      :options="versions"
      option-value="versionId"
      style="width: 120px"
      class="nav-input"
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
    </q-select>

    <version-creator
      :open="openCreateVersion"
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
import { Typography, FlexBox, TextButton, ListItem } from "@/components/common";
import { VersionCreator } from "@/components/project/selector";

const versions = ref<VersionSchema[]>([]);
const openCreateVersion = ref(false);

const project = computed(() => projectStore.project);
const isProjectDefined = computed(() => projectStore.isProjectDefined);
const projectName = computed(() =>
  isProjectDefined.value ? project.value.name : "No Project Selected"
);

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
