<template>
  <q-select
    v-model="getProjectApiStore.currentProject"
    outlined
    dark
    :options-dark="darkMode"
    label="Project"
    :options="projectStore.allProjects"
    option-value="projectId"
    option-label="name"
    :class="className"
    color="primary"
    @popup-show="handleReload"
  >
    <template #option="{ opt, itemProps }">
      <list-item v-bind="itemProps" :title="opt.name" :data-cy-name="opt.name">
        <template #actions>
          <flex-box justify="end">
            <icon-button
              v-if="permissionStore.isAllowed('project.edit_members', opt)"
              small
              :tooltip="`Invite to ${opt.name}`"
              icon="invite"
              data-cy="button-project-invite"
              @click="projectInviteId = opt.projectId"
            />
            <icon-button
              v-if="permissionStore.isAllowed('project.edit', opt)"
              small
              :tooltip="`Edit ${opt.name}`"
              icon="edit"
              data-cy="button-project-edit"
              @click="identifierSaveStore.selectIdentifier(opt, 'save')"
            />
            <icon-button
              v-if="permissionStore.isAllowed('project.delete', opt)"
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
        v-if="permissionStore.isAllowed('safa.view')"
        text
        block
        label="Add Project"
        icon="add"
        @click="identifierSaveStore.selectIdentifier(undefined, 'save')"
      />
      <invite-member-modal
        :open="!!projectInviteId"
        :entity="entity"
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
import { computed, ref } from "vue";
import { MemberEntitySchema } from "@/types";
import {
  getProjectApiStore,
  identifierSaveStore,
  permissionStore,
  projectStore,
  useTheme,
} from "@/hooks";
import { FlexBox, IconButton, ListItem, TextButton } from "@/components/common";
import { InviteMemberModal } from "@/components/members";

const { darkMode } = useTheme();

const projectInviteId = ref<string>();

const entity = computed(
  () =>
    ({
      entityId: projectStore.projectId,
      entityType: "PROJECT",
    } as MemberEntitySchema)
);

const className = computed(() =>
  projectStore.isProjectDefined ? "nav-input nav-multi-input-left" : "nav-input"
);
/**
 * Reloads the project list and resets any selected project.
 */
function handleReload() {
  projectInviteId.value = undefined;

  getProjectApiStore.handleReload();
}
</script>
