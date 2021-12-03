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
        @refresh="retrieveMembers"
        class="mt-5"
      >
        <template v-slot:addItemDialogue>
          <settings-add-member-modal
            :is-open="isOpen"
            :project="project"
            @onCancel="isOpen = false"
            @onConfirm="onConfirm"
          />
        </template>
      </generic-selector>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Project, ProjectMember, ProjectRole } from "@/types";
import { GenericSelector } from "@/components";
import { getProjectMembers } from "@/api";
import SettingsAddMemberModal from "./SettingsAddMemberModal.vue";
import { sessionModule } from "@/store";

/**
 * List the members of given project within the settings.
 * TODO: Show delete and other admin operations if admin or above
 */
export default Vue.extend({
  components: { GenericSelector, SettingsAddMemberModal },
  props: {
    project: {
      type: Object as PropType<Project>,
      required: true,
    },
  },
  data() {
    return {
      members: [] as ProjectMember[],
      isLoading: false,
      isOpen: false,
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
    onAddMember() {
      this.isOpen = true;
    },
    async onConfirm(): Promise<void> {
      this.isOpen = true;
      await this.retrieveMembers();
    },
  },
});
</script>
