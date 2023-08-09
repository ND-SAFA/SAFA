<template>
  <panel-card
    title="Project Members"
    subtitle="Edit and invite project members."
    :minimal="props.minimal"
  >
    <selector-table
      :columns="membersColumns"
      :rows="rows"
      row-key="email"
      addable
      :deletable="isAdmin"
      :editable="isAdmin"
      :loading="memberApiStore.loading"
      @row:add="handleAdd"
      @row:edit="handleEdit"
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
        <icon-button
          v-if="membersColumns.length > 1 && row.email === userEmail"
          icon="leave"
          tooltip="Leave project"
          data-cy="button-selector-leave"
          @click="handleDelete(row)"
        />
      </template>
    </selector-table>
    <project-member-modal
      :open="modalOpen"
      :member="editedMember"
      :email="addedMember"
      @close="handleClose"
      @submit="handleClose"
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
import { MembershipSchema, ProjectRole } from "@/types";
import { membersColumns } from "@/util";
import {
  logStore,
  memberApiStore,
  membersStore,
  projectStore,
  sessionStore,
} from "@/hooks";
import { PanelCard, SelectorTable, IconButton } from "@/components/common";
import ProjectMemberModal from "./ProjectMemberModal.vue";

const props = defineProps<{
  /**
   * Whether the table should be displayed minimally.
   */
  minimal?: boolean;
}>();

const editedMember = ref<MembershipSchema>();
const addedMember = ref<string | null>(null);
const modalOpen = ref(false);

const project = computed(() => projectStore.project);

const isAdmin = computed(() => sessionStore.isAdmin(project.value));

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
  editedMember.value = undefined;
  modalOpen.value = false;
}

/**
 * Opens the invite member modal.
 * @param email - The member email to invite.
 */
function handleAdd(email: string | null): void {
  addedMember.value = email;
  modalOpen.value = true;
}

/**
 * Opens the edit member modal.
 * @param member - The member to edit.
 */
function handleEdit(member: MembershipSchema): void {
  editedMember.value = member;
  modalOpen.value = true;
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
