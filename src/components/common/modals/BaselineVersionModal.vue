<template>
  <project-version-stepper-modal
    v-model="currentStep"
    title="Select Baseline Project Version"
    :isOpen="isOpen"
    v-bind:isLoading.sync="isLoading"
    v-bind:project.sync="selectedProject"
    v-bind:version.sync="selectedVersion"
    @onSubmit="onSubmit"
    @onClose="$emit('onClose')"
  />
</template>

<script lang="ts">
import Vue from "vue";
import { ProjectIdentifier, ProjectVersion } from "@/types";
import { getProjectVersion } from "@/api";
import { appModule, projectModule } from "@/store";
import ProjectVersionStepperModal from "./ProjectVersionStepperModal.vue";

export default Vue.extend({
  name: "baseline-version-modal",
  components: {
    ProjectVersionStepperModal,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      isLoading: false,
      selectedProject: undefined as ProjectIdentifier | undefined,
      selectedVersion: undefined as ProjectVersion | undefined,
      currentStep: 1,
    };
  },
  methods: {
    onSubmit() {
      if (this.selectedProject === undefined) {
        appModule.onWarning("Please select a project to update");
      } else if (this.selectedVersion === undefined) {
        appModule.onWarning("Please select a baseline version");
      } else {
        this.isLoading = true;

        getProjectVersion(this.selectedVersion.versionId)
          .then(projectModule.setProjectCreationResponse)
          .finally(() => {
            this.isLoading = false;
            this.$emit("onClose");
          });
      }
    },
  },
});
</script>
