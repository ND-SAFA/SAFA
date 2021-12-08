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
        @item:add="onAddMember"
        @item:edit="onEditMember"
        @item:delete="onDeleteMember"
        @refresh="retrieveMembers"
        class="mt-5"
      >
        <template v-slot:addItemDialogue>
          <settings-member-information-modal
            :is-open="isNewOpen"
            :project="project"
            @cancel="isNewOpen = false"
            @confirm="onConfirmAdd"
          />
        </template>
        <template v-slot:editItemDialogue>
          <settings-member-information-modal
            :is-open="isEditOpen"
            :clear-on-close="false"
            :project="project"
            :member="memberToEdit"
            @cancel="isEditOpen = false"
            @confirm="onConfirmEdit"
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
import { GenericSelector } from "@/components";
import { deleteProjectMember, getProjectMembers } from "@/api";
import SettingsMemberInformationModal from "./SettingsMemberInformationModal.vue";
import { appModule, sessionModule } from "@/store";

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
      members: [] as ProjectMembership[],
      memberToEdit: undefined as ProjectMembership | undefined,
      isLoading: false,
      isNewOpen: false,
      isEditOpen: false,
    };
  },
  computed: {
    isAdmin(): boolean {
      const userEmail = sessionModule.authenticationToken.sub;
      const allowedRoles = [ProjectRole.ADMIN, ProjectRole.OWNER];

      return (
        this.members.filter(
          (m) => m.email === userEmail && allowedRoles.includes(m.role)
        ).length > 0
      );
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
  watch: {
    project() {
      this.retrieveMembers();
    },
  },
  created() {
    this.retrieveMembers();
  },
  methods: {
    async retrieveMembers(): Promise<void> {
      if (this.project.projectId !== "") {
        this.isLoading = true;
        this.members = await getProjectMembers(this.project.projectId);
        this.isLoading = false;
      }
    },
    onAddMember(): void {
      this.isNewOpen = true;
    },
    onEditMember(member: ProjectMembership): void {
      this.memberToEdit = member;
      this.isEditOpen = true;
    },
    onDeleteMember(member: ProjectMembership): void {
      appModule.SET_CONFIRMATION_MESSAGE({
        type: ConfirmationType.INFO,
        title: "Remove User from Project",
        body: `Are you sure you want to remove ${member.email} from project?`,
        statusCallback: async (isConfirmed: boolean) => {
          if (isConfirmed) {
            await deleteProjectMember(member);
            await this.retrieveMembers();
          }
        },
      });
    },
    async onConfirmAdd(): Promise<void> {
      this.isNewOpen = false;
      await this.retrieveMembers();
    },
    async onConfirmEdit(): Promise<void> {
      this.isEditOpen = false;
      await this.retrieveMembers();
    },
  },
});
</script>
