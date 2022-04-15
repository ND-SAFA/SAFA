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
import {
  ConfirmationType,
  Project,
  ProjectMembership,
  ProjectRole,
} from "@/types";
import { GenericSelector } from "@/components/common/generic";
import { deleteProjectMember, getProjectMembers } from "@/api";
import SettingsMemberInformationModal from "./SettingsMemberInformationModal.vue";
import { logModule, sessionModule } from "@/store";

/**
 * List the members of given project within the settings.
 */
export default Vue.extend({
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
    };
  },
  computed: {
    isAdmin(): boolean {
      const userEmail = sessionModule.userEmail;
      const allowedRoles = [ProjectRole.ADMIN, ProjectRole.OWNER];
      const userQuery = this.project.members.filter(
        (m) => m.email === userEmail && allowedRoles.includes(m.role)
      );
      return userQuery.length === 1;
    },
    members(): ProjectMembership[] {
      return this.project.members;
    },
    hasDescription(): boolean {
      const description = this.project.description;
      return description !== "";
    },
    headers() {
      return [
        { text: "Email", value: "email", sortable: false, isSelectable: false },
        {
          text: "Role",
          value: "role",
          sortable: true,
          isSelectable: true,
        },
        { text: "Actions", value: "actions", sortable: false },
      ];
    },
  },
  methods: {
    async handleRetrieveMembers(): Promise<void> {
      if (this.project.projectId !== "") {
        this.isLoading = true;
        this.members = await getProjectMembers(this.project.projectId);
        this.isLoading = false;
      }
    },
    handleAddMember(): void {
      this.isNewOpen = true;
    },
    handleEditMember(member: ProjectMembership): void {
      this.memberToEdit = member;
      this.isEditOpen = true;
    },
    handleDeleteMember(member: ProjectMembership): void {
      logModule.SET_CONFIRMATION_MESSAGE({
        type: ConfirmationType.INFO,
        title: "Remove User from Project",
        body: `Are you sure you want to remove ${member.email} from project?`,
        statusCallback: async (isConfirmed: boolean) => {
          if (isConfirmed) {
            await deleteProjectMember(member);
          }
        },
      });
    },
    async handleConfirmAdd(): Promise<void> {
      this.isNewOpen = false;
    },
    async handleConfirmEdit(): Promise<void> {
      this.isEditOpen = false;
    },
  },
});
</script>
