<template>
  <q-select
    v-if="isProjectDefined"
    v-model="getVersionApiStore.currentVersion"
    outlined
    dark
    :options-dark="darkMode"
    options-selected-class="primary"
    label="Version"
    :options="allVersions"
    option-value="versionId"
    class="nav-input nav-version q-mx-sm"
    color="accent"
    @popup-show="getVersionApiStore.handleReload"
  >
    <template #selected>
      {{ versionToString(getVersionApiStore.currentVersion) }}
    </template>
    <template #option="{ opt, itemProps }">
      <list-item
        v-bind="itemProps"
        :title="versionToString(opt)"
        :action-cols="2"
      >
        <template #actions>
          <flex-box justify="end">
            <icon-button
              v-if="deletable"
              small
              :tooltip="`Delete ${versionToString(opt)}`"
              icon="delete"
              data-cy="button-version-delete"
              @click="handleDelete(opt)"
            />
          </flex-box>
        </template>
      </list-item>
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
      <create-version-modal
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
import {
  getVersionApiStore,
  projectApiStore,
  projectStore,
  sessionStore,
  useTheme,
} from "@/hooks";
import { TextButton, ListItem, IconButton, FlexBox } from "@/components/common";
import { CreateVersionModal } from "@/components/project/creator";

const openCreateVersion = ref(false);

const { darkMode } = useTheme();

const allVersions = computed(() => getVersionApiStore.allVersions);
const project = computed(() => projectStore.project);
const isProjectDefined = computed(() => projectStore.isProjectDefined);
const deletable = computed(
  () => sessionStore.isEditor(project.value) && allVersions.value.length > 1
);

/**
 * Adds the new version the version list and loads that version.
 * @param version - The new version.
 */
async function handleVersionCreated(version: VersionSchema): Promise<void> {
  openCreateVersion.value = false;
  await getVersionApiStore.handleLoad(version.versionId);
}

/**
 * Attempts to delete the version.
 * @param version - The version to delete.
 */
function handleDelete(version: VersionSchema) {
  projectApiStore.handleDeleteVersion(version, {
    onSuccess: async () => getVersionApiStore.handleReload(),
  });
}
</script>
