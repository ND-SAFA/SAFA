<template>
  <v-container class="px-10">
    <v-row>
      <v-col :cols="store.isFTA ? 12 : 5">
        <typography el="h1" variant="subtitle" value="Artifact" />
        <v-divider class="mb-2" />
        <v-text-field
          filled
          v-if="!store.isFTA"
          v-model="store.editedArtifact.name"
          label="Artifact Name"
          hint="Please select an identifier for the artifact"
          :error-messages="nameError"
          :loading="nameCheckIsLoading"
          data-cy="input-artifact-name"
        />
        <artifact-type-input
          persistent-hint
          v-if="!store.isFTA && !store.isSafetyCase && !store.isFMEA"
          v-model="store.editedArtifact.type"
          label="Artifact Type"
          hint="Required"
          data-cy="input-artifact-type"
        />
        <v-select
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
        />
      </v-col>
      <v-col cols="7" v-if="!store.isFTA">
        <typography el="h1" variant="subtitle" value="Description" />
        <v-divider class="mb-2" />
        <v-textarea
          filled
          persistent-hint
          v-if="!store.isFTA"
          label="Artifact Body"
          v-model="store.editedArtifact.body"
          rows="3"
          hint="Required"
          data-cy="input-artifact-body"
        />
        <v-textarea
          filled
          v-if="!store.isFTA"
          label="Artifact Summary"
          v-model="store.editedArtifact.summary"
          rows="3"
          hint="A brief summary of the artifact content"
          data-cy="input-artifact-summary"
        />
      </v-col>
    </v-row>
    <custom-field-input v-if="store.isFMEA" v-model="store.editedArtifact" />
  </v-container>
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
  CustomFieldInput,
  Typography,
} from "@/components/common";

/**
 * Inputs for artifact creation.
 */
export default Vue.extend({
  name: "ArtifactCreatorInputs",
  components: {
    ArtifactTypeInput,
    CustomFieldInput,
    ArtifactInput,
    Typography,
  },
  data() {
    return {
      nameError: "",
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

      this.nameCheckIsLoading = true;
      artifactSaveStore.isNameValid = false;
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
              this.nameError = artifactSaveStore.isNameValid
                ? ""
                : "Name is already used, please select another.";
            })
            .catch(() => {
              artifactSaveStore.isNameValid = false;
              this.nameCheckIsLoading = false;
              this.nameError = "";
            });
        }
      }, 500);
    },
    "store.isNameValid"() {
      artifactSaveStore.updateCanSave();
    },
    "store.parentId"() {
      artifactSaveStore.updateCanSave();
    },
    "store.editedArtifact.type"() {
      artifactSaveStore.updateArtifactType();
    },
    "store.editedArtifact": {
      deep: true,
      handler() {
        artifactSaveStore.updateCanSave();
      },
    },
  },
});
</script>
