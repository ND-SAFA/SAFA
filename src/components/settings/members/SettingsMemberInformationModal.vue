<template>
  <modal :is-open="isOpen" :title="modelTitle" @close="handleCancel">
    <template #body>
      <flex-box align="center" t="4">
        <v-text-field
          v-model="userEmail"
          filled
          label="User Email"
          class="mr-1"
          style="min-width: 300px"
          :readonly="member !== undefined"
          :rules="emailRules"
          data-cy="settings-input-user-email"
          @update:error="handleErrorUpdate"
        />
        <v-select
          v-model="userRole"
          filled
          label="Role"
          :items="projectRoles"
          item-value="id"
          item-text="name"
          data-cy="settings-input-user-role"
        />
      </flex-box>
      <project-input v-if="!member" v-model="projectIds" multiple />
    </template>
    <template #actions>
      <v-spacer />
      <v-btn
        :disabled="!validated"
        color="primary"
        data-cy="button-add-user-to-project"
        @click="handleConfirm"
      >
        {{ buttonLabel }}
      </v-btn>
    </template>
  </modal>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { MembershipSchema, ProjectRole } from "@/types";
import { projectRoleOptions } from "@/util";
import { projectStore } from "@/hooks";
import { handleInviteMember } from "@/api";
import { Modal, FlexBox, ProjectInput } from "@/components/common";

/**
 * The modal for sharing a project with a user.
 */
export default defineComponent({
  name: "SettingsMemberInformation",
  components: { ProjectInput, FlexBox, Modal },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    member: {
      type: Object as PropType<MembershipSchema>,
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
      projectIds: [projectStore.projectId],
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
      projectRoles: projectRoleOptions(),
    };
  },
  computed: {
    /**
     * @return The label for the modal.
     */
    modelTitle(): string {
      return this.member ? "Edit Member" : "Share Project";
    },
    /**
     * @return The label for the submit button.
     */
    buttonLabel(): string {
      return this.member ? "Save" : "Add To Project";
    },
    /**
     * @return Whether the user is validated.
     */
    validated(): boolean {
      return (
        !this.hasErrors &&
        this.userEmail.length > 0 &&
        this.projectIds.length > 0 &&
        this.userRole !== undefined
      );
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
    member(newMember: MembershipSchema | undefined): void {
      if (!newMember) return;

      this.userRole = newMember.role;
      this.userEmail = newMember.email;
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
      this.projectIds = [projectStore.projectId];
    },
    /**
     * Attempts to save a change to a project member.
     */
    async handleConfirm() {
      this.projectIds.forEach((projectId: string) => {
        if (!this.validated || !this.userRole) return;

        handleInviteMember(projectId, this.userEmail, this.userRole, {
          onSuccess: () => this.$emit("confirm"),
        });
      });
    },
    /**
     * Closes the modal.
     */
    handleCancel() {
      this.$emit("cancel");
    },
  },
});
</script>
