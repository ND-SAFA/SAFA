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
import { GenericFileSelector } from "@/components/common";
import { saveProject, handleUploadProjectVersion } from "@/api";
import { logModule } from "@/store";

/**
 * Togglable input for project files.
 *
 * @emits-1 `update:files` (File[]) - On flat files updated.
 * @emits-2 `close` - On close.
 */
export default Vue.extend({
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
    isDisabled(): boolean {
      return this.name.length === 0 || this.selectedFiles.length === 0;
    },
  },
  methods: {
    handleChangeFiles(files: File[]) {
      this.selectedFiles = files;
    },
    async handleCreate() {
      try {
        this.isLoading = true;

        const project = await saveProject({
          projectId: "",
          name: this.name,
          description: this.description,
        });

        await handleUploadProjectVersion(
          project.project.projectId,
          project.projectVersion.versionId,
          this.selectedFiles,
          true
        );

        this.selectedFiles = [];
      } catch (e) {
        logModule.onDevWarning(e);
        logModule.onError("Unable to create a project from these files");
      } finally {
        this.isLoading = false;
      }
    },
  },
  watch: {
    selectedFiles(files: File[]) {
      this.$emit("update:files", files);
    },
  },
});
</script>
