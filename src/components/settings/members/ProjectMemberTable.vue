<template>
  <panel-card
    title="Project Members"
    subtitle="Edit and invite project members."
  >
    <selector-table
      :columns="membersColumns"
      :rows="rows"
      row-key="email"
      addable
      :deletable="isAdmin"
      :editable="isAdmin"
      :loading="memberApiStore.loading"
      @row:add="modalOpen = true"
      @row:edit="handleEdit"
      @row:delete="handleDelete"
      @refresh="handleRefresh"
    >
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
      @close="modalOpen = false"
      @submit="modalOpen = false"
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

const editedMember = ref<MembershipSchema>();
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
