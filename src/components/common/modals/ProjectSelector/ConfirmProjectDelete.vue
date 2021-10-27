<template>
  <GenericModal size="xs" :isOpen="isOpen" :title="title" @onClose="onCancel">
    <template v-slot:body>
      <v-container>
        <v-row justify="center">
          <v-col align-self="center">
            <v-text-field
              v-model="confirmText"
              :label="textboxLabel"
              class="ma-3"
              rounded
              solo
              dense
            />
          </v-col>
        </v-row>
      </v-container>
    </template>
    <template v-slot:actions>
      <v-container>
        <v-row justify="center">
          <v-btn :disabled="!validated" color="error" @click="onConfirm">
            {{ submitButtonLabel }}
          </v-btn>
        </v-row>
      </v-container>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import { ProjectIdentifier } from "@/types/domain/project";
import Vue, { PropType } from "vue";
import GenericModal from "@/components/common/modals/GenericModal.vue";
export default Vue.extend({
  components: { GenericModal },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: false,
    },
  },
  data() {
    return {
      confirmText: "",
      textboxLabel: "",
      title: "",
      validated: false,
      submitButtonLabel: "",
    };
  },
  methods: {
    clearData(): void {
      this.confirmText = "";
      this.validated = false;
    },
    onConfirm() {
      const project = this.$props.project;
      if (this.validated) {
        this.$emit("onConfirmDelete", project);
      }
    },
    onCancel() {
      this.$emit("onCancelDelete");
    },
  },
  watch: {
    project(project: ProjectIdentifier) {
      if (project !== undefined) {
        this.textboxLabel = `Type "${project.name}"`;
        this.title = `Confirm project name: ${project.name}`;
        this.submitButtonLabel = `Delete Project ${project.name}`;
      }
    },
    confirmText() {
      const project = this.$props.project;
      if (project !== undefined) {
        if (this.confirmText === project.name) {
          this.validated = true;
          return;
        }
      }
      this.validated = false;
    },
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.clearData();
      }
    },
  },
});
</script>
