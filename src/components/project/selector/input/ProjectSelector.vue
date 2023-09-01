<template>
  <q-select
    v-model="getProjectApiStore.currentProject"
    outlined
    dark
    :options-dark="darkMode"
    label="Project"
    :options="getProjectApiStore.allProjects"
    option-value="projectId"
    option-label="name"
    class="nav-input"
    color="primary"
    @popup-show="handleReload"
  >
    <template #option="{ opt, itemProps }">
      <list-item v-bind="itemProps" :title="opt.name" :data-cy-name="opt.name">
        <template #actions>
          <flex-box justify="end">
            <icon-button
              v-if="permissionStore.projectAllows('editor', opt)"
              small
              :tooltip="`Invite to ${opt.name}`"
              icon="invite"
              data-cy="button-project-invite"
              @click="projectInviteId = opt.projectId"
            />
            <icon-button
              v-if="permissionStore.projectAllows('editor', opt)"
              small
              :tooltip="`Edit ${opt.name}`"
              icon="edit"
              data-cy="button-project-edit"
              @click="identifierSaveStore.selectIdentifier(opt, 'save')"
            />
            <icon-button
              v-if="permissionStore.projectAllows('owner', opt)"
              small
              :tooltip="`Delete ${opt.name}`"
              icon="delete"
              data-cy="button-project-delete"
              @click="identifierSaveStore.selectIdentifier(opt, 'delete')"
            />
          </flex-box>
        </template>
      </list-item>
    </template>
    <template #after-options>
      <text-button
        v-if="permissionStore.organizationAllows('navigation')"
        text
        block
        label="Add Project"
        icon="add"
        @click="identifierSaveStore.selectIdentifier(undefined, 'save')"
      />
      <project-member-modal
        :open="!!projectInviteId"
        :project-id="projectInviteId"
        @close="projectInviteId = undefined"
        @submit="projectInviteId = undefined"
      />
    </template>
  </q-select>
</template>

<script lang="ts">
/**
 Displays the current project, and allows it to be changed.
 */
export default {
  name: "ProjectSelector",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import {
  getProjectApiStore,
  identifierSaveStore,
  permissionStore,
  useTheme,
} from "@/hooks";
import { FlexBox, IconButton, ListItem, TextButton } from "@/components/common";
import { ProjectMemberModal } from "@/components/settings";

const { darkMode } = useTheme();

const projectInviteId = ref<string>();

/**
 * Reloads the project list and resets any selected project.
 */
function handleReload() {
  projectInviteId.value = undefined;

  getProjectApiStore.handleReload();
}
</script>
