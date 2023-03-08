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
      :loading="loading"
      @row:add="modalOpen = true"
      @row:edit="handleEdit"
      @row:delete="handleDelete"
      @refresh="handleRefresh"
    />
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
import { logStore, membersStore, projectStore, sessionStore } from "@/hooks";
import { handleDeleteMember, handleGetMembers } from "@/api";
import { PanelCard } from "@/components/common";
import SelectorTable from "@/components/common/table/SelectorTable.vue";
import ProjectMemberModal from "./ProjectMemberModal.vue";

const editedMember = ref<MembershipSchema | undefined>();
const loading = ref(false);
const modalOpen = ref(false);

const project = computed(() => projectStore.project);

const isAdmin = computed(() => sessionStore.isAdmin(project.value));

const rows = computed(() => membersStore.members);

/**
 * Loads the project's members.
 */
async function handleRefresh(): Promise<void> {
  if (project.value.projectId === "") return;

  loading.value = true;

  handleGetMembers().then(() => (loading.value = false));
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
 * Opens the delete member modal.
 * @param member - The member to delete.
 */
function handleDelete(member: MembershipSchema): void {
  if (
    member.role === ProjectRole.OWNER &&
    rows.value.filter(({ role }) => role === ProjectRole.OWNER).length === 1
  ) {
    logStore.onInfo("You cannot delete the only owner of this project.");
  } else {
    handleDeleteMember(member);
  }
}
</script>
