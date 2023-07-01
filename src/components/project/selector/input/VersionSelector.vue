<template>
  <q-select
    v-if="isProjectDefined"
    v-model="getVersionApiStore.currentVersion"
    outlined
    dark
    :options-dark="darkMode"
    options-selected-class="primary"
    label="Version"
    :options="getVersionApiStore.allVersions"
    option-value="versionId"
    class="nav-input nav-version q-ml-sm"
    color="accent"
    @popup-show="getVersionApiStore.handleReload"
  >
    <template #selected>
      {{ versionToString(getVersionApiStore.currentVersion) }}
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
import { computed, ref } from "vue";
import { VersionSchema } from "@/types";
import { versionToString } from "@/util";
import { getVersionApiStore, projectStore, useTheme } from "@/hooks";
import { TextButton, ListItem } from "@/components/common";
import { VersionCreator } from "@/components/project/creator";

const openCreateVersion = ref(false);

const { darkMode } = useTheme();

const project = computed(() => projectStore.project);
const isProjectDefined = computed(() => projectStore.isProjectDefined);

/**
 * Adds the new version the version list and loads that version.
 * @param version - The new version.
 */
async function handleVersionCreated(version: VersionSchema): Promise<void> {
  openCreateVersion.value = false;
  await getVersionApiStore.handleLoad(version.versionId);
}
</script>
