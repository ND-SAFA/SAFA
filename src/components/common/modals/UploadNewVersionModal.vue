<template>
  <ProjectVersionStepperModal
    v-model="currentStep"
    title="Upload Flat Files"
    :isOpen="isOpen"
    :afterSteps="[['Upload Files', filesSelected.length > 0]]"
    v-bind:isLoading.sync="isLoading"
    v-bind:project.sync="selectedProject"
    v-bind:version.sync="selectedVersion"
    @onSubmit="onSubmit"
    @onClose="onClose"
  >
    <template v-slot:afterItems>
      <v-stepper-content step="3">
        <GenericFileSelector
          v-if="selectedVersion !== undefined"
          @onChangeFiles="onChangeFiles"
        />
      </v-stepper-content>
    </template>

    <template v-slot:action:main>
      <v-checkbox
        v-if="currentStep === 3"
        v-model="setAsNewVersion"
        color="secondary"
      >
        <template v-slot:label>
          <label style="color: black" class="ma-0 pa-0">
            Set as current version
          </label>
        </template>
      </v-checkbox>
    </template>
  </ProjectVersionStepperModal>
</template>

<script lang="ts">
import { ProjectIdentifier, ProjectVersion } from "@/types/domain/project";
import Vue from "vue";
import GenericFileSelector from "@/components/common/generic/GenericFileSelector.vue";
import { uploadNewProjectVersion } from "@/api/handlers/upload-version-handler";
import ProjectVersionStepperModal from "@/components/common/modals/ProjectVersionStepperModal.vue";

export default Vue.extend({
  name: "UploadNewVersionModal",
  components: {
    GenericFileSelector,
    ProjectVersionStepperModal,
  },
  props: {
    isOpen: Boolean,
  },
  data() {
    return {
      currentStep: 1,
      selectedProject: undefined as ProjectIdentifier | undefined,
      selectedVersion: undefined as ProjectVersion | undefined,
      filesSelected: [] as File[],
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
});
</script>
