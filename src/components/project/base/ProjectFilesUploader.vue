<template>
  <div>
    <project-identifier-input
      v-bind:name.sync="identifier.name"
      v-bind:description.sync="identifier.description"
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
import { IdentifierSchema } from "@/types";
import { identifierSaveStore } from "@/hooks";
import { handleBulkImportProject } from "@/api";
import { GenericSwitch } from "@/components/common";
import ProjectFilesInput from "./ProjectFilesInput.vue";
import ProjectIdentifierInput from "./ProjectIdentifierInput.vue";

/**
 * Creates projects with bulk uploaded files.
 *
 * @emits-1 `submit` - On project creation submitted.
 */
export default Vue.extend({
  name: "ProjectFilesUploader",
  components: {
    ProjectFilesInput,
    GenericSwitch,
    ProjectIdentifierInput,
  },
  props: {
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
     * @return  The identifier being updated.
     */
    identifier(): IdentifierSchema {
      return identifierSaveStore.editedIdentifier;
    },
    /**
     * Whether the submit button is disabled.
     */
    isDisabled(): boolean {
      const isNameInvalid = this.identifier.name.length === 0;

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

      handleBulkImportProject(this.identifier, this.selectedFiles, {
        onSuccess: () => {
          this.selectedFiles = [];
          this.isLoading = false;
          this.$emit("submit");
        },
        onError: () => {
          this.isLoading = false;
        },
      });
    },
  },
});
</script>
