<template>
  <v-container>
    <typography el="h2" variant="subtitle" value="Project Members" />
    <generic-selector
      is-open
      :headers="headers"
      :items="members"
      :has-delete="isAdmin"
      :has-edit="isAdmin"
      :has-select="false"
      :is-loading="isLoading"
      item-key="email"
      class="mt-5"
      @item:add="handleAddMember"
      @item:edit="handleEditMember"
      @item:delete="handleDeleteMember"
      @refresh="handleRetrieveMembers"
    >
      <template v-slot:addItemDialogue>
        <settings-member-information-modal
          :is-open="isNewOpen"
          @cancel="handleConfirmAdd"
          @confirm="handleConfirmAdd"
        />
      </template>
      <template v-slot:editItemDialogue>
        <settings-member-information-modal
          :is-open="isEditOpen"
          :clear-on-close="false"
          :member="memberToEdit"
          @cancel="handleConfirmEdit"
          @confirm="handleConfirmEdit"
        />
      </template>
    </generic-selector>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { MembershipModel, ProjectModel, ProjectRole } from "@/types";
import { logStore, projectStore, sessionStore } from "@/hooks";
import { handleDeleteMember, handleGetMembers } from "@/api";
import { GenericSelector, Typography } from "@/components/common";
import SettingsMemberInformationModal from "./SettingsMemberInformationModal.vue";

/**
 * List the members of given project within the settings.
 */
export default Vue.extend({
  name: "SettingsMembers",
  components: { GenericSelector, SettingsMemberInformationModal, Typography },
  data() {
    return {
      memberToEdit: undefined as MembershipModel | undefined,
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
    project(): ProjectModel {
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
    members(): MembershipModel[] {
      return this.project.members;
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
    handleEditMember(member: MembershipModel): void {
      this.memberToEdit = member;
      this.isEditOpen = true;
    },
    /**
     * Opens the delete member modal.
     * @param member - The member to delete.
     */
    handleDeleteMember(member: MembershipModel): void {
      if (
        member.role === ProjectRole.OWNER &&
        this.members.filter(({ role }) => role === ProjectRole.OWNER).length ===
          1
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
