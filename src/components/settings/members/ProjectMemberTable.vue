<template>
  <panel-card
    title="Project Members"
    subtitle="Manage and invite project members."
    :minimal="props.minimal"
  >
    <template #title-actions>
      <text-button
        v-if="addMode"
        text
        label="Cancel"
        icon="cancel"
        @click="handleClose"
      />
    </template>

    <selector-table
      v-if="!addMode"
      :columns="membersColumns"
      :rows="rows"
      row-key="email"
      addable
      :deletable="isAdmin"
      :loading="memberApiStore.loading"
      @row:add="handleAdd"
      @row:delete="handleDelete"
      @refresh="handleRefresh"
    >
      <template #search-append="{ search }">
        <icon-button
          v-if="!!search"
          small
          tooltip="Invite member"
          icon="invite"
          @click="handleAdd(search)"
        />
      </template>

      <template #cell-actions="{ row }">
        <member-role-button
          v-if="isAdmin"
          :member="row"
          :project-id="projectStore.projectId"
        />
        <icon-button
          v-if="row.email === userEmail"
          icon="leave"
          tooltip="Leave project"
          data-cy="button-member-leave"
          @click="handleDelete(row)"
        />
      </template>
    </selector-table>

    <invite-member-inputs
      v-else
      :project-id="projectStore.projectId"
      :email="addedMember"
      @save="handleClose"
    />
  </panel-card>
</template>

<script lang="ts">
/**
 * List the members of given project within the settings.
 */
export default {
  name: "ProjectMemberTable",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { MembershipSchema, MinimalProps, ProjectRole } from "@/types";
import { membersColumns } from "@/util";
import {
  logStore,
  memberApiStore,
  membersStore,
  permissionStore,
  projectStore,
  sessionStore,
} from "@/hooks";
import {
  PanelCard,
  SelectorTable,
  IconButton,
  TextButton,
} from "@/components/common";
import InviteMemberInputs from "./InviteMemberInputs.vue";
import MemberRoleButton from "./MemberRoleButton.vue";

const props = defineProps<MinimalProps>();

const addedMember = ref<string | null>(null);
const addMode = ref(false);

const project = computed(() => projectStore.project);

const isAdmin = computed(() =>
  permissionStore.projectAllows("admin", project.value)
);

const rows = computed(() => membersStore.members);

const userEmail = computed(() => sessionStore.user?.email);

const ownerCount = computed(
  () => rows.value.filter((member) => member.role === ProjectRole.OWNER).length
);

/**
 * Loads the project's members.
 */
async function handleRefresh(): Promise<void> {
  if (project.value.projectId === "") return;

  await memberApiStore.handleReload();
}

/**
 * Clears all member modal state.
 */
function handleClose(): void {
  addedMember.value = "";
  addMode.value = false;
}

/**
 * Opens the invite member modal.
 * @param email - The member email to invite.
 */
function handleAdd(email: string | null): void {
  addedMember.value = email;
  addMode.value = true;
}

/**
 * Opens the delete member modal, if the member is not the only owner.
 * @param member - The member to delete.
 */
function handleDelete(member: MembershipSchema): void {
  if (member.role === ProjectRole.OWNER && ownerCount.value === 1) {
    logStore.onInfo("You cannot remove the only owner of this project.");
  } else {
    memberApiStore.handleDelete(member);
  }
}
</script>
