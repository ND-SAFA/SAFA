<template>
  <panel-card>
    <typography el="h2" variant="subtitle" value="Project Members" />
    <table-selector
      is-open
      :headers="headers"
      :items="members"
      :has-delete="isAdmin"
      :has-edit="isAdmin"
      :is-loading="isLoading"
      item-key="email"
      class="mt-5"
      @item:add="handleAddMember"
      @item:edit="handleEditMember"
      @item:delete="handleDeleteMember"
      @refresh="handleRetrieveMembers"
    >
      <template #addItemDialogue>
        <settings-member-information-modal
          :is-open="isNewOpen"
          @cancel="handleConfirmAdd"
          @confirm="handleConfirmAdd"
        />
      </template>
      <template #editItemDialogue>
        <settings-member-information-modal
          :is-open="isEditOpen"
          :clear-on-close="false"
          :member="memberToEdit"
          @cancel="handleConfirmEdit"
          @confirm="handleConfirmEdit"
        />
      </template>
    </table-selector>
  </panel-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { MembershipSchema, ProjectSchema, ProjectRole } from "@/types";
import { logStore, membersStore, projectStore, sessionStore } from "@/hooks";
import { handleDeleteMember, handleGetMembers } from "@/api";
import { TableSelector, Typography, PanelCard } from "@/components/common";
import SettingsMemberInformationModal from "./SettingsMemberInformationModal.vue";

/**
 * List the members of given project within the settings.
 */
export default defineComponent({
  name: "SettingsMembers",
  components: {
    PanelCard,
    TableSelector,
    SettingsMemberInformationModal,
    Typography,
  },
  data() {
    return {
      memberToEdit: undefined as MembershipSchema | undefined,
      isLoading: false,
      isNewOpen: false,
      isEditOpen: false,
      headers: [
        { text: "Email", value: "email" },
        { text: "Role", value: "role" },
        { text: "Actions", value: "actions", sortable: false },
      ],
    };
  },
  computed: {
    /**
     * @return The current project.
     */
    project(): ProjectSchema {
      return projectStore.project;
    },
    /**
     * @return Whether the current user is an admin.
     */
    isAdmin(): boolean {
      return sessionStore.isAdmin(this.project);
    },
    /**
     * @return All project members.
     */
    members(): MembershipSchema[] {
      return membersStore.members;
    },
  },
  methods: {
    /**
     * Loads the project's members.
     */
    async handleRetrieveMembers(): Promise<void> {
      if (this.project.projectId === "") return;

      this.isLoading = true;
      handleGetMembers().then(() => (this.isLoading = false));
    },
    /**
     * Opens the add member modal.
     */
    handleAddMember(): void {
      this.isNewOpen = true;
    },
    /**
     * Opens the edit member modal.
     * @param member - The member to edit.
     */
    handleEditMember(member: MembershipSchema): void {
      this.memberToEdit = member;
      this.isEditOpen = true;
    },
    /**
     * Opens the delete member modal.
     * @param member - The member to delete.
     */
    handleDeleteMember(member: MembershipSchema): void {
      if (
        member.role === ProjectRole.OWNER &&
        this.members.filter(
          ({ role }: MembershipSchema) => role === ProjectRole.OWNER
        ).length === 1
      ) {
        logStore.onInfo("You cannot delete the only owner of this project.");
      } else {
        handleDeleteMember(member);
      }
    },
    /**
     * Closes the add member modal.
     */
    async handleConfirmAdd(): Promise<void> {
      this.isNewOpen = false;
    },
    /**
     * Closes the edit member modal.
     */
    async handleConfirmEdit(): Promise<void> {
      this.isEditOpen = false;
    },
  },
});
</script>
