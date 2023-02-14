<template>
  <div class="mt-4">
    <v-row dense>
      <v-col cols="6">
        <v-text-field
          v-if="!store.isFTA"
          v-model="store.editedArtifact.name"
          filled
          label="Artifact Name"
          hint="Please select an identifier for the artifact"
          :error-messages="nameErrors"
          :loading="nameCheckIsLoading"
          data-cy="input-artifact-name"
      /></v-col>
      <v-col cols="6">
        <artifact-type-input
          v-if="!store.isFTA && !store.isSafetyCase && !store.isFMEA"
          v-model="store.editedArtifact.type"
          persistent-hint
          label="Artifact Type"
          hint="Required"
          data-cy="input-artifact-type"
      /></v-col>
    </v-row>

    <v-textarea
      v-if="!store.isFTA"
      v-model="store.editedArtifact.body"
      filled
      persistent-hint
      label="Artifact Body"
      rows="3"
      hint="Required"
      data-cy="input-artifact-body"
    />

    <v-select
      v-if="displayDocumentType"
      v-model="store.editedArtifact.documentType"
      filled
      label="Document Type"
      :items="documentTypes"
      item-text="name"
      item-value="id"
      hint="Which type of document this artifact belongs to"
      data-cy="input-artifact-document"
    />
    <v-select
      v-if="store.isSafetyCase"
      v-model="store.editedArtifact.safetyCaseType"
      filled
      label="Safety Case Type"
      :items="safetyCaseTypes"
      item-text="name"
      item-value="id"
      data-cy="input-artifact-sc"
    />
    <v-select
      v-if="store.isFTA"
      v-model="store.editedArtifact.logicType"
      filled
      label="Logic Type"
      :items="logicTypes"
      item-text="name"
      item-value="id"
      data-cy="input-artifact-logic"
    />
    <artifact-input
      v-if="!store.isUpdate"
      v-model="store.parentId"
      only-document-artifacts
      :multiple="false"
      label="Parent Artifact"
      data-cy="input-artifact-parent"
      class="mb-4"
    />

    <attribute-list-input :artifact="store.editedArtifact" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
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
export default defineComponent({
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
