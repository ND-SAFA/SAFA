<template>
  <v-container style="max-width: 30em">
    <generic-switch
      class="mt-0"
      v-model="emptyFiles"
      label="Create an empty project"
    />
    <project-files-input
      v-if="!emptyFiles"
      v-model="selectedFiles"
      data-cy="input-files-bulk"
    />
    <v-btn
      block
      color="primary"
      :disabled="isDisabled"
      @click="handleCreate"
      :loading="isLoading"
      data-cy="button-create-project"
    >
      Create Project From Files
    </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { handleBulkImportProject } from "@/api";
import { GenericSwitch } from "@/components/common";
import ProjectFilesInput from "./ProjectFilesInput.vue";

/**
 * Togglable input for uploading project files.
 *
 * @emits-1 `update:files` (File[]) - On flat files updated.
 */
export default Vue.extend({
  name: "ProjectFilesUploader",
  components: {
    ProjectFilesInput,
    GenericSwitch,
  },
  props: {
    name: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      selectedFiles: [] as File[],
      isLoading: false,
      emptyFiles: false,
    };
  },

  computed: {
    /**
     * Whether the submit button is disabled.
     */
    isDisabled(): boolean {
      return (
        this.name.length === 0 ||
        (this.selectedFiles.length === 0 && !this.emptyFiles)
      );
    },
  },
  methods: {
    /**
     * Attempts to save the project.
     */
    async handleCreate() {
      this.isLoading = true;

      handleBulkImportProject(
        {
          projectId: "",
          name: this.name,
          description: this.description,
        },
        this.selectedFiles,
        {
          onSuccess: () => {
            this.selectedFiles = [];
            this.isLoading = false;
            this.$emit("update:name", "");
            this.$emit("update:description", "");
          },
          onError: () => {
            this.isLoading = false;
          },
        }
      );
    },
  },
  watch: {
    /**
     * Emits changes to selected files.
     */
    selectedFiles(files: File[]) {
      this.$emit("update:files", files);
    },
  },
});
</script>
