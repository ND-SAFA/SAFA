<template>
  <GenericModal
    title="Upload Flat Files"
    :isOpen="isOpen"
    :actionsHeight="125"
    :isLoading="isLoading"
    @onClose="onClose"
  >
    <template v-slot:body>
      <v-row justify="center" class="mt-5">
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
      </v-row>
      <v-row>
        <v-container>
          <v-row justify="center">
            <h3 style="text-align: center" class="mt-10">
              3. Upload flat files
            </h3>
          </v-row>
          <v-row justify="center">
            <file-selector
              v-if="selectedVersion !== undefined"
              :validated="filesReady"
              @onChangeFiles="onChangeFiles"
            />
            <p v-else>Project version not selected.</p>
          </v-row>
        </v-container>
      </v-row>
    </template>
    <template v-slot:actions>
      <v-container class="ma-0 pa-0">
        <v-row class="ma-0 pa-0">
          <v-col class="ma-0 pa-0">
            <v-row class="ma-0 pa-0" justify="center">
              <v-checkbox v-model="setAsNewVersion" color="secondary">
                <template v-slot:label>
                  <label style="color: black" class="ma-0 pa-0">
                    Set as current version
                  </label>
                </template>
              </v-checkbox>
            </v-row>
            <v-row class="ma-0 pa-0" justify="center">
              <v-btn @click="onSubmit" color="primary">
                Submit <v-icon id="upload-button">mdi-upload</v-icon>
              </v-btn>
            </v-row>
          </v-col>
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
import FileSelector from "@/components/common/modals/UploadNewVersionModal/FileSelector.vue";
import { uploadNewProjectVersion } from "@/api/handlers/upload-version-handler";
import ProjectAndVersionSelector from "@/components/common/modals/ProjectAndVersionModal.vue";
import GenericModal from "@/components/common/modals/GenericModal.vue";
import { projectModule } from "@/store";
export default Vue.extend({
  components: {
    FileSelector,
    ProjectAndVersionSelector,
    GenericModal,
  },
  props: {
    isOpen: Boolean,
  },
  data() {
    return {
      fileSelectorOpen: false,
      filesSelected: [] as File[],
      selectedProject: undefined as ProjectIdentifier | undefined,
      selectedVersion: undefined as ProjectVersion | undefined,
      filesReady: false,
      isLoading: false,
      setAsNewVersion: true,
    };
  },
  methods: {
    onClose() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.filesSelected = [];
      this.$emit("onClose");
    },
    onChangeFiles(files: File[]) {
      this.filesSelected = files;
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
      uploadNewProjectVersion(
        this.selectedProject,
        this.selectedVersion,
        this.filesSelected,
        this.setAsNewVersion,
        () => (this.isLoading = true),
        () => (this.isLoading = false),
        this.onClose
      );
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
  },
});
</script>
