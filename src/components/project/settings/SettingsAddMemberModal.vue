<template>
  <generic-modal size="xs" :is-open="isOpen" :title="title" @close="onCancel">
    <template v-slot:body>
      <v-container>
        <v-row justify="center">
          <v-col align-self="center">
            <v-text-field
              v-model="newUserEmail"
              label="User Email"
              class="ma-3"
              rounded
              solo
              dense
              :rules="emailRules"
              @update:error="onErrorUpdate"
            />
            <button-row :definitions="buttonDefinition" />
          </v-col>
        </v-row>
      </v-container>
    </template>
    <template v-slot:actions>
      <v-container>
        <v-row justify="center">
          <v-btn :disabled="!validated" color="error" @click="onConfirm">
            Add to Project
          </v-btn>
        </v-row>
      </v-container>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import {
  ButtonDefinition,
  ButtonType,
  EmptyLambda,
  ProjectIdentifier,
  ProjectRole,
} from "@/types";
import Vue, { PropType } from "vue";
import { GenericModal } from "@/components/common";
import ButtonRow from "@/components/common/button-row/ButtonRow.vue";
import { capitalize, getEnumKeys } from "@/util";
import { addProjectMember } from "@/api";
import { appModule } from "@/store";

/**
 * The modal for sharing a project with a user.
 */
export default Vue.extend({
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
  },
  data() {
    return {
      newUserEmail: "",
      newUserRole: undefined as ProjectRole | undefined,
      submitButtonLabel: "",
      hasErrors: false,
      emailRules: [
        (v: string) =>
          !v ||
          /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) ||
          "E-mail must be valid",
      ],
    };
  },
  computed: {
    validated(): boolean {
      return (
        !this.hasErrors &&
        this.newUserEmail.length > 0 &&
        this.newUserRole !== undefined
      );
    },
    projectRoles(): string[] {
      return getEnumKeys(ProjectRole);
    },
    itemLambdas(): EmptyLambda[] {
      return this.projectRoles.map((role) => {
        return () => {
          this.newUserRole = this.getProjectRole(role);
        };
      });
    },
    buttonDefinition(): ButtonDefinition[] {
      return [
        {
          type: ButtonType.LIST_MENU,
          label: "Project Role",
          menuItems: this.projectRoles,
          menuHandlers: this.itemLambdas,
          buttonColor: "primary",
          buttonIsText: false,
          showSelectedValue: true,
        },
      ];
    },
  },
  methods: {
    onErrorUpdate(hasErrors: boolean): void {
      this.hasErrors = hasErrors;
    },
    clearData(): void {
      this.newUserEmail = "";
    },
    async onConfirm() {
      const project = this.$props.project;
      const projectId = this.project?.projectId;
      const projectRole = this.newUserRole;
      if (
        this.validated &&
        projectId !== undefined &&
        projectRole !== undefined
      ) {
        addProjectMember(projectId, this.newUserEmail, projectRole)
          .then(() => this.$emit("onConfirm", project))
          .catch();
      } else {
        appModule.onWarning("Please define project role.");
      }
    },
    onCancel() {
      this.$emit("onCancel");
    },
    getProjectRole(role: string): ProjectRole {
      return ProjectRole[role.toUpperCase() as keyof typeof ProjectRole];
    },
  },
  watch: {
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.clearData();
      }
    },
  },
});
</script>
