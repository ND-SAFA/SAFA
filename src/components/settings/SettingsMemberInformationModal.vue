<template>
  <generic-modal :is-open="isOpen" :title="title" @close="handleCancel">
    <template v-slot:body>
      <v-row dense class="mt-4">
        <v-col>
          <v-text-field
            v-model="userEmail"
            label="User Email"
            rounded
            solo
            dense
            style="min-width: 300px"
            :readonly="member !== undefined"
            :rules="emailRules"
            @update:error="handleErrorUpdate"
          />
        </v-col>
        <v-col>
          <button-row :definitions="buttonDefinition" />
        </v-col>
      </v-row>
    </template>
    <template v-slot:actions>
      <v-container>
        <v-row justify="center">
          <v-btn :disabled="!validated" color="error" @click="handleConfirm">
            Add to Project
          </v-btn>
        </v-row>
      </v-container>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  ButtonDefinition,
  ButtonMenuItem,
  ButtonType,
  ListMenuDefinition,
  ProjectIdentifier,
  ProjectMembership,
  ProjectRole,
} from "@/types";
import { logModule } from "@/store";
import { handleInviteMember } from "@/api";
import { GenericModal, ButtonRow } from "@/components/common";

/**
 * The modal for sharing a project with a user.
 */
export default Vue.extend({
  name: "SettingsMemberInformation",
  components: { ButtonRow, GenericModal },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: true,
    },
    title: {
      type: String,
      default: "Share Project",
    },
    member: {
      type: Object as PropType<ProjectMembership>,
      required: false,
    },
    clearOnClose: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  data() {
    return {
      userEmail: "",
      userRole: undefined as ProjectRole | undefined,
      submitButtonLabel: "",
      hasErrors: false,
      emailRules: [
        (v: string) =>
          !v ||
          /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) ||
          "E-mail must be valid",
      ],
      projectRoles: [
        ProjectRole.OWNER,
        ProjectRole.ADMIN,
        ProjectRole.EDITOR,
        ProjectRole.VIEWER,
      ],
    };
  },
  computed: {
    /**
     * @return Whether the user is validated.
     */
    validated(): boolean {
      return (
        !this.hasErrors &&
        this.userEmail.length > 0 &&
        this.userRole !== undefined
      );
    },
    /**
     * @return All project role menu items.
     */
    menuItems(): ButtonMenuItem[] {
      return this.projectRoles.map((role) => ({
        name: role,
        onClick: () => {
          this.userRole = this.getProjectRole(role);
        },
      }));
    },
    /**
     * @return The project menu button.
     */
    buttonDefinition(): ButtonDefinition[] {
      return [
        {
          type: ButtonType.LIST_MENU,
          label: "Project Role",
          menuItems: this.menuItems,
          buttonColor: "primary",
          buttonIsText: false,
          showSelectedValue: true,
          selectedItem: this.userRole,
        } as ListMenuDefinition,
      ];
    },
  },
  methods: {
    /**
     * Handles any errors.
     * @param hasErrors - Whether there are errors.
     */
    handleErrorUpdate(hasErrors: boolean): void {
      this.hasErrors = hasErrors;
    },
    /**
     * Clears modal data.
     */
    clearData(): void {
      this.userEmail = "";
      this.userRole = undefined;
    },
    /**
     * Attempts to save a change to a project member.
     */
    async handleConfirm() {
      const project = this.$props.project;
      const projectId = this.project?.projectId;
      const projectRole = this.userRole;
      if (
        this.validated &&
        projectId !== undefined &&
        projectRole !== undefined
      ) {
        handleInviteMember(projectId, this.userEmail, projectRole, {
          onSuccess: () => this.$emit("confirm", project),
        });
      } else {
        logModule.onWarning("Please define project role.");
      }
    },
    /**
     * Closes the modal.
     */
    handleCancel() {
      this.$emit("cancel");
    },
    /**
     * Returns the correct role id for a role.
     * @param role - The role to find.
     */
    getProjectRole(role: string): ProjectRole {
      return ProjectRole[role.toUpperCase() as keyof typeof ProjectRole];
    },
  },
  watch: {
    /**
     * Clears the modal data when opened.
     */
    isOpen(open: boolean) {
      if (!open || !this.clearOnClose) return;

      this.clearData();
    },
    /**
     * Updates member fields when the member changes.
     * @param newMember - The new member.
     */
    member(newMember: ProjectMembership | undefined): void {
      if (!newMember) return;

      this.userRole = newMember.role;
      this.userEmail = newMember.email;
    },
  },
});
</script>
