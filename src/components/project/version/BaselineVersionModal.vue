<template>
  <project-version-stepper-modal
    v-model="currentStep"
    :title="title"
    :isOpen="isOpen"
    :startStep="startStep"
    v-bind:isLoading.sync="isLoading"
    v-bind:project.sync="selectedProject"
    v-bind:version.sync="selectedVersion"
    @submit="onSubmit"
    @close="$emit('close')"
  />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ProjectIdentifier, ProjectVersion } from "@/types";
import { logModule } from "@/store";
import { handleLoadVersion } from "@/api";
import ProjectVersionStepperModal from "./ProjectVersionStepperModal.vue";

/**
 * Stepper for setting the current project and version.
 *
 * @emits `close` - Emitted when modal is exited or project + version set.
 */
export default Vue.extend({
  name: "BaselineVersionModal",
  components: {
    ProjectVersionStepperModal,
  },
  props: {
    /**
     * Whether the current component should be in open.
     */
    isOpen: {
      type: Boolean,
      required: true,
    },
    /**
     * The title of the modal encapsulating this component.
     */
    title: {
      type: String,
      default: "Select Baseline Project Version",
    },
    /**
     * Optional project which if defined begins the stepper on version selection
     * fetching the versions of given project.
     */
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: false,
    },
  },
  data() {
    return {
      currentStep: this.project === undefined ? 1 : 2,
      selectedVersion: undefined as ProjectVersion | undefined,
      selectedProject: this.project,
      isLoading: false,
    };
  },
  computed: {
    /**
     * @return The start step, which skips the project selection if one is already given.
     */
    startStep(): number {
      return this.project === undefined ? 1 : 2;
    },
  },
  watch: {
    /**
     * Sets the selected project and moves to the next step when opened with an existing project.
     */
    isOpen(open: boolean) {
      if (!open || !this.project) return;

      this.selectedProject = this.project;
      this.currentStep = 2;
    },
  },
  methods: {
    /**
     * Loads the selected project version.
     */
    async onSubmit() {
      if (this.selectedProject === undefined) {
        logModule.onWarning("Please select a project to update.");
      } else if (this.selectedVersion === undefined) {
        logModule.onWarning("Please select a baseline version.");
      } else {
        this.isLoading = true;

        await handleLoadVersion(this.selectedVersion.versionId);

        this.isLoading = false;
        this.$emit("close");
      }
    },
  },
});
</script>
