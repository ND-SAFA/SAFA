<template>
  <div>
    <project-identifier-input
      v-bind:name.sync="currentName"
      v-bind:description.sync="currentDescription"
      :data-cy-name="dataCyName"
      :data-cy-description="dataCyDescription"
    />
    <v-container style="max-width: 40em">
      <generic-switch
        class="mt-0"
        v-model="emptyFiles"
        label="Create an empty project"
        data-cy="toggle-create-empty-project"
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
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { handleBulkImportProject } from "@/api";
import { GenericSwitch } from "@/components/common";
import ProjectFilesInput from "./ProjectFilesInput.vue";
import ProjectIdentifierInput from "./ProjectIdentifierInput.vue";

/**
 * Togglable input for uploading project files.
 *
 * @emits-1 `update:name` (string) - On name updated.
 * @emits-2 `update:description` (string) - On description updated.
 * @emits-3 `update:files` (File[]) - On flat files updated.
 * @emits-3 `submit` - On project creation submitted.
 */
export default Vue.extend({
  name: "ProjectFilesUploader",
  components: {
    ProjectFilesInput,
    GenericSwitch,
    ProjectIdentifierInput,
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
    dataCyName: {
      type: String,
      default: "input-project-name",
    },
    dataCyDescription: {
      type: String,
      default: "input-project-description",
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
     * Emits changes to the name.
     */
    currentName: {
      get(): string {
        return this.name;
      },
      set(newName: string): void {
        this.$emit("update:name", newName);
      },
    },
    /**
     * Emits changes to the description.
     */
    currentDescription: {
      get(): string {
        return this.description;
      },
      set(newDescription: string): void {
        this.$emit("update:description", newDescription);
      },
    },
    /**
     * Whether the submit button is disabled.
     */
    isDisabled(): boolean {
      const isNameInvalid = this.name.length === 0;

      if (this.emptyFiles) {
        return isNameInvalid;
      } else {
        return (
          isNameInvalid ||
          (this.selectedFiles.length === 0 && !this.emptyFiles) ||
          !this.selectedFiles.find(({ name }) => name === "tim.json")
        );
      }
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
            this.$emit("submit");
            this.$emit("update:name", "");
            this.$emit("update:description", "");
            this.$emit("update:files", []);
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
