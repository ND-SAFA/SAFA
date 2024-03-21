<template>
  <q-select
    v-model="getVersionApiStore.currentProject"
    standout
    bg-color="transparent"
    class="nav-breadcrumb"
    label="Project"
    :options="projectStore.allProjects"
    :loading="getVersionApiStore.loadLoading"
    option-value="projectId"
    option-label="name"
    @popup-show="handleReload"
  >
    <template #option="{ opt, itemProps }: { opt: ProjectSchema }">
      <list-item v-bind="itemProps" :title="opt.name" :data-cy-name="opt.name">
        <template #actions>
          <flex-box justify="end">
            <icon-button
              v-if="permissionStore.isAllowed('project.edit_members', opt)"
              small
              :tooltip="`Invite to ${opt.name}`"
              icon="member-add"
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
import { MemberEntitySchema, ProjectSchema } from "@/types";
import {
  getProjectApiStore,
  getVersionApiStore,
  identifierSaveStore,
  permissionStore,
  projectStore,
} from "@/hooks";
import { FlexBox, IconButton, ListItem, TextButton } from "@/components/common";
import { InviteMemberModal } from "@/components/members";

const projectInviteId = ref<string>();

const entity = computed(
  () =>
    ({
      entityId: projectInviteId.value,
      entityType: "PROJECT",
    }) as MemberEntitySchema
);

/**
 * Reloads the project list and resets any selected project.
 */
function handleReload() {
  projectInviteId.value = undefined;

  getProjectApiStore.handleLoadProjects();
}
</script>
