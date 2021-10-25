<template>
  <GenericModal
    title="Select Project and Baseline Version"
    :isOpen="isOpen"
    :isLoading="isLoading"
    @onClose="onClose"
  >
    <template v-slot:body>
      <ProjectAndVersionSelector
        :selectedProject="selectedProject"
        :selectedVersion="selectedVersion"
        :isOpen="isOpen"
        projectSelectorTitle="1. Select a Project to Modify"
        @onProjectSelected="selectProject"
        @onProjectUnselected="unselectProject"
        versionSelectorTitle="2. Select a Version to Upload To"
        @onVersionSelected="selectVersion"
        @onVersionUnselected="unselectVersion"
      />
    </template>
    <template v-slot:actions>
      <v-container class="ma-0 pa-0">
        <v-row justify="center" class="ma-10">
          <v-btn @click="onSubmit" color="primary ">
            Save <v-icon id="upload-button">mdi-check</v-icon>
          </v-btn>
        </v-row>
      </v-container>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import {
  Project,
  ProjectIdentifier,
  ProjectVersion,
} from "@/types/domain/project";
import Vue from "vue";
import { getProjectVersion } from "@/api/project-api";
import ProjectAndVersionSelector from "@/components/common/modals/ProjectAndVersionModal.vue";
import GenericModal from "@/components/common/modals/GenericModal.vue";
import { appModule, projectModule } from "@/store";

export default Vue.extend({
  name: "baseline-version-modal",
  components: {
    ProjectAndVersionSelector,
    GenericModal,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      fileSelectorOpen: false,
      selectedProject: undefined as ProjectIdentifier | undefined,
      selectedVersion: undefined as ProjectVersion | undefined,
      filesReady: false,
      isLoading: false,
    };
  },
  methods: {
    clearData() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.filesReady = false;
      this.isLoading = false;
      this.fileSelectorOpen = false;
    },
    onClose() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.$emit("onClose");
    },
    selectProject(project: ProjectIdentifier) {
      this.selectedProject = project;
    },
    unselectProject() {
      this.selectedProject = undefined;
    },
    selectVersion(version: ProjectVersion) {
      this.selectedVersion = version;
    },
    unselectVersion() {
      this.selectedVersion = undefined;
    },
    onSubmit() {
      if (this.selectedProject === undefined) {
        appModule.onWarning("Please select a project to update");
      } else if (this.selectedVersion === undefined) {
        appModule.onWarning("Please select a baseline version");
      } else {
        getProjectVersion(this.selectedVersion.versionId)
          .then(async (res) => {
            await projectModule.setProjectCreationResponse(res);
            this.isLoading = false;
            this.$emit("onClose");
          })
          .finally(() => {
            this.isLoading = false;
            this.$emit("onClose");
          });
      }
    },
  },
  computed: {
    project(): Project {
      return projectModule.getProject;
    },
  },
  watch: {
    selectedVersion() {
      if (this.selectedVersion !== undefined) {
        this.filesReady = true;
      }
    },
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.clearData();
      }
    },
  },
});
</script>
