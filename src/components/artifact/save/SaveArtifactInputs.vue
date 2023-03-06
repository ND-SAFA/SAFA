<template>
  <div class="mt-4">
    <v-row dense>
      <v-col cols="6">
        <v-text-field
          filled
          v-if="!store.isFTA"
          v-model="store.editedArtifact.name"
          label="Artifact Name"
          hint="Please select an identifier for the artifact"
          :error-messages="nameErrors"
          :loading="nameCheckIsLoading"
          data-cy="input-artifact-name"
      /></v-col>
      <v-col cols="6">
        <artifact-type-input
          persistent-hint
          v-if="!store.isFTA && !store.isSafetyCase && !store.isFMEA"
          v-model="store.editedArtifact.type"
          label="Artifact Type"
          hint="Required"
          data-cy="input-artifact-type"
      /></v-col>
    </v-row>

    <v-textarea
      v-if="!store.isFTA"
      filled
      persistent-hint
      label="Artifact Body"
      v-model="store.editedArtifact.body"
      rows="3"
      hint="Required"
      data-cy="input-artifact-body"
    />

    <v-select
      v-if="displayDocumentType"
      filled
      label="Document Type"
      v-model="store.editedArtifact.documentType"
      :items="documentTypes"
      item-text="name"
      item-value="id"
      hint="Which type of document this artifact belongs to"
      data-cy="input-artifact-document"
    />
    <v-select
      filled
      v-if="store.isSafetyCase"
      label="Safety Case Type"
      v-model="store.editedArtifact.safetyCaseType"
      :items="safetyCaseTypes"
      item-text="name"
      item-value="id"
      data-cy="input-artifact-sc"
    />
    <v-select
      filled
      v-if="store.isFTA"
      label="Logic Type"
      v-model="store.editedArtifact.logicType"
      :items="logicTypes"
      item-text="name"
      item-value="id"
      data-cy="input-artifact-logic"
    />
    <artifact-input
      only-document-artifacts
      v-if="!store.isUpdate"
      v-model="store.parentId"
      :multiple="false"
      label="Parent Artifact"
      data-cy="input-artifact-parent"
      class="mb-4"
    />

    <attribute-list-input :artifact="store.editedArtifact" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { SelectOption } from "@/types";
import { documentTypeMap, logicTypeOptions, safetyCaseOptions } from "@/util";
import { artifactSaveStore, documentStore, projectStore } from "@/hooks";
import { getDoesArtifactExist } from "@/api";
import {
  ArtifactInput,
  ArtifactTypeInput,
  AttributeListInput,
} from "@/components/common";

/**
 * Inputs for artifact creation and editing.
 */
export default Vue.extend({
  name: "SaveArtifactInputs",
  components: {
    AttributeListInput,
    ArtifactTypeInput,
    ArtifactInput,
  },
  data() {
    return {
      nameCheckTimer: undefined as ReturnType<typeof setTimeout> | undefined,
      nameCheckIsLoading: false,

      safetyCaseTypes: safetyCaseOptions(),
      logicTypes: logicTypeOptions(),
    };
  },
  computed: {
    /**
     * @return The document types allowed on the current document.
     */
    documentTypes(): SelectOption[] {
      return documentTypeMap()[documentStore.currentType];
    },
    /**
     * @return Whether to display the document type input.
     */
    displayDocumentType(): boolean {
      return this.documentTypes.length > 1;
    },
    /**
     * @return The document types allowed on the current document.
     */
    nameErrors(): string[] {
      return this.nameCheckIsLoading ? [] : artifactSaveStore.nameErrors;
    },
    /**
     * @return The artifact save store.
     */
    store(): typeof artifactSaveStore {
      return artifactSaveStore;
    },
  },
  watch: {
    /**
     * Checks for name conflicts when the name changes.
     */
    "store.editedArtifact.name"(newName: string): void {
      if (this.nameCheckTimer) {
        clearTimeout(this.nameCheckTimer);
      }

      artifactSaveStore.isNameValid = false;
      this.nameCheckIsLoading = true;
      this.nameCheckTimer = setTimeout(() => {
        if (!newName) {
          artifactSaveStore.isNameValid = false;
          this.nameCheckIsLoading = false;
        } else if (!artifactSaveStore.hasNameChanged) {
          artifactSaveStore.isNameValid = true;
          this.nameCheckIsLoading = false;
        } else {
          getDoesArtifactExist(projectStore.versionId, newName)
            .then((nameExists) => {
              artifactSaveStore.isNameValid = !nameExists;
              this.nameCheckIsLoading = false;
            })
            .catch(() => {
              artifactSaveStore.isNameValid = false;
              this.nameCheckIsLoading = false;
            });
        }
      }, 500);
    },
    "store.editedArtifact.type"() {
      artifactSaveStore.updateArtifactType();
    },
  },
});
</script>
