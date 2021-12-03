<template>
  <v-row>
    <v-col>
      <h2>Members</h2>
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
        @add-item="onAddMember"
        @edit-item="onEditMember"
        @delete-item="onDeleteMember"
        @refresh="retrieveMembers"
        class="mt-5"
      >
        <template v-slot:addItemDialogue>
          <settings-member-information-modal
            :is-open="isNewOpen"
            :project="project"
            @onCancel="isNewOpen = false"
            @onConfirm="onConfirm"
          />
        </template>
        <template v-slot:editItemDialogue>
          <settings-member-information-modal
            :is-open="isEditOpen"
            :clear-on-close="false"
            :project="project"
            :member="memberToEdit"
            @onCancel="isEditOpen = false"
            @onConfirm="onConfirm"
          />
        </template>
      </generic-selector>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ConfirmationType, Project, ProjectMember, ProjectRole } from "@/types";
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
      members: [] as ProjectMember[],
      memberToEdit: undefined as ProjectMember | undefined,
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
    onEditMember(member: ProjectMember): void {
      this.memberToEdit = member;
      this.isEditOpen = true;
    },
    onDeleteMember(member: ProjectMember): void {
      appModule.SET_CONFIRMATION_MESSAGE({
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
    async onConfirm(): Promise<void> {
      this.isNewOpen = true;
      await this.retrieveMembers();
    },
  },
});
</script>
