<template>
  <v-container style="max-width: 30em">
    <generic-file-selector @change:files="handleChangeFiles" />
    <v-btn
      block
      color="primary"
      :disabled="isDisabled"
      @click="handleCreate"
      :loading="isLoading"
    >
      Create Project From Files
    </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { handleBulkImportProject } from "@/api";
import { GenericFileSelector } from "@/components/common";

/**
 * Togglable input for project files.
 *
 * @emits-1 `update:files` (File[]) - On flat files updated.
 * @emits-2 `close` - On close.
 */
export default Vue.extend({
  name: "ProjectFilesInput",
  components: {
    GenericFileSelector,
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
    };
  },
  computed: {
    /**
     * Whether the submit button is disabled.
     */
    isDisabled(): boolean {
      return this.name.length === 0 || this.selectedFiles.length === 0;
    },
  },
  methods: {
    /**
     * Saves changed files.
     * @param files - The changed files.
     */
    handleChangeFiles(files: File[]) {
      this.selectedFiles = files;
    },
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
