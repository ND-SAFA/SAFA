<template>
  <v-row>
    <v-col>
      <h2 class="text-h5">Members</h2>
      <v-divider />
      <generic-selector
        :headers="headers"
        :items="members"
        :is-open="true"
        :has-delete="isAdmin"
        :has-edit="isAdmin"
        :has-select="false"
        :is-loading="isLoading"
        item-key="email"
        @item:add="handleAddMember"
        @item:edit="handleEditMember"
        @item:delete="handleDeleteMember"
        @refresh="handleRetrieveMembers"
        class="mt-5"
      >
        <template v-slot:addItemDialogue>
          <settings-member-information-modal
            :is-open="isNewOpen"
            :project="project"
            @cancel="isNewOpen = false"
            @confirm="handleConfirmAdd"
          />
        </template>
        <template v-slot:editItemDialogue>
          <settings-member-information-modal
            :is-open="isEditOpen"
            :clear-on-close="false"
            :project="project"
            :member="memberToEdit"
            @cancel="isEditOpen = false"
            @confirm="handleConfirmEdit"
          />
        </template>
      </generic-selector>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Project, ProjectMembership, ProjectRole } from "@/types";
import { sessionModule } from "@/store";
import { getProjectMembers, handleDeleteMember } from "@/api";
import { GenericSelector } from "@/components/common/generic";
import SettingsMemberInformationModal from "./SettingsMemberInformationModal.vue";

/**
 * List the members of given project within the settings.
 */
export default Vue.extend({
  name: "SettingsMemberSection",
  components: { GenericSelector, SettingsMemberInformationModal },
  props: {
    project: {
      type: Object as PropType<Project>,
      required: true,
    },
  },
  data() {
    return {
      memberToEdit: undefined as ProjectMembership | undefined,
      isLoading: false,
      isNewOpen: false,
      isEditOpen: false,
      headers: [
        { text: "Email", value: "email", sortable: false, isSelectable: false },
        {
          text: "Role",
          value: "role",
          sortable: true,
          isSelectable: true,
        },
        { text: "Actions", value: "actions", sortable: false },
      ],
    };
  },
  computed: {
    /**
     * @return Whether the current user is an admin.
     */
    isAdmin(): boolean {
      const userEmail = sessionModule.userEmail;
      const allowedRoles = [ProjectRole.ADMIN, ProjectRole.OWNER];
      const userQuery = this.project.members.filter(
        (m) => m.email === userEmail && allowedRoles.includes(m.role)
      );
      return userQuery.length === 1;
    },
    /**
     * @return All project members.
     */
    members() {
      return this.project.members;
    },
    /**
     * @return Whether the project has a description.
     */
    hasDescription(): boolean {
      return this.project.description !== "";
    },
  },
  methods: {
    /**
     * Loads the project's members.
     */
    async handleRetrieveMembers(): Promise<void> {
      if (this.project.projectId !== "") {
        this.isLoading = true;
        this.members = await getProjectMembers(this.project.projectId);
        this.isLoading = false;
      }
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
    handleEditMember(member: ProjectMembership): void {
      this.memberToEdit = member;
      this.isEditOpen = true;
    },
    /**
     * Opens the delete member modal.
     * @param member - The member to delete.
     */
    handleDeleteMember(member: ProjectMembership): void {
      handleDeleteMember(member);
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
