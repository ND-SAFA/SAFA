<template>
  <v-container style="max-width: 30em">
    <v-switch
      v-model="doUploadFlatFiles"
      label="Upload Flat Files"
      @change:files="onChangeFiles"
    />
    <generic-file-selector
      v-if="doUploadFlatFiles"
      @change:files="onChangeFiles"
    />
    <v-btn
      v-if="doUploadFlatFiles"
      block
      color="primary"
      :disabled="isDisabled"
      @click="onCreate"
      :loading="isLoading"
    >
      Create Project From Files
    </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { GenericFileSelector } from "@/components/common";
import { saveOrUpdateProject, uploadNewProjectVersion } from "@/api";
import { logModule } from "@/store";

/**
 * Togglable input for project files.
 *
 * @emits-1 `update:open` (Boolean) - On toggle open.
 * @emits-2 `update:files` (File[]) - On flat files updated.
 * @emits-3 `close` - On close.
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
      doUploadFlatFiles: false,
      isLoading: false,
    };
  },
  computed: {
    isDisabled(): boolean {
      return this.name.length === 0 || this.selectedFiles.length === 0;
    },
  },
  methods: {
    onChangeFiles(files: File[]) {
      this.selectedFiles = files;
    },
    async onCreate() {
      try {
        this.isLoading = true;

        const project = await saveOrUpdateProject({
          projectId: "",
          name: this.name,
          description: this.description,
        });

        await uploadNewProjectVersion(
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
    doUploadFlatFiles(doUpload: boolean) {
      if (!doUpload) {
        this.selectedFiles = [];
      }

      this.$emit("update:open", doUpload);
    },
    selectedFiles(files: File[]) {
      this.$emit("update:files", files);
    },
  },
});
</script>
