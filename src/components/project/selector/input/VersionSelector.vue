<template>
  <q-select
    v-if="isProjectDefined"
    v-model="getVersionApiStore.currentVersion"
    standout
    bg-color="transparent"
    class="nav-breadcrumb"
    options-selected-class="primary"
    label="Version"
    :options="allVersions"
    option-value="versionId"
    @popup-show="getVersionApiStore.handleLoadVersions()"
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
              @click="getVersionApiStore.handleDelete(opt)"
            />
          </flex-box>
        </template>
      </list-item>
    </template>
    <template #after-options>
      <text-button
        v-if="displayActions"
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
import { getVersionApiStore, permissionStore, projectStore } from "@/hooks";
import { TextButton, ListItem, IconButton, FlexBox } from "@/components/common";
import { CreateVersionModal } from "@/components/project/creator";

const openCreateVersion = ref(false);

const allVersions = computed(() => projectStore.allVersions);
const project = computed(() => projectStore.project);
const isProjectDefined = computed(() => projectStore.isProjectDefined);

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_versions")
);
const deletable = computed(
  () => displayActions.value && allVersions.value.length > 1
);

/**
 * Adds the new version the version list and loads that version.
 * @param version - The new version.
 */
async function handleVersionCreated(version: VersionSchema): Promise<void> {
  openCreateVersion.value = false;
  await getVersionApiStore.handleLoad(version.versionId);
}
</script>
