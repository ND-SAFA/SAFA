<template>
  <v-container class="px-10">
    <v-row>
      <v-col :cols="isFTA ? 12 : 5">
        <typography el="h1" variant="subtitle" value="Artifact" />
        <v-divider class="mb-2" />
        <v-text-field
          filled
          v-if="!isFTA"
          v-model="artifact.name"
          label="Artifact Name"
          hint="Please select an identifier for the artifact"
          :error-messages="nameError"
          :loading="nameCheckIsLoading"
        />
        <v-combobox
          filled
          persistent-hint
          v-if="!isFTA && !isSafetyCase && !isFMEA"
          v-model="artifact.type"
          :items="artifactTypes"
          label="Artifact Type"
          hint="Required"
        />
        <v-select
          filled
          label="Document Type"
          v-model="artifact.documentType"
          :items="documentTypes"
          item-text="name"
          item-value="id"
          hint="Which type of document this artifact belongs to"
        />
        <v-select
          filled
          v-if="isSafetyCase"
          label="Safety Case Type"
          v-model="artifact.safetyCaseType"
          :items="safetyCaseTypes"
          item-text="name"
          item-value="id"
        />
        <v-select
          filled
          v-if="isFTA"
          label="Logic Type"
          v-model="artifact.logicType"
          :items="logicTypes"
          item-text="name"
          item-value="id"
        />
        <artifact-input
          only-document-artifacts
          v-if="!isEditMode"
          v-model="parentId"
          :multiple="false"
          label="Parent Artifact"
        />
      </v-col>
      <v-col cols="7" v-if="!isFTA">
        <typography el="h1" variant="subtitle" value="Description" />
        <v-divider class="mb-2" />
        <v-textarea
          filled
          persistent-hint
          v-if="!isFTA"
          label="Artifact Body"
          v-model="artifact.body"
          rows="3"
          hint="Required"
        />
        <v-textarea
          filled
          v-if="!isFTA"
          label="Artifact Summary"
          v-model="artifact.summary"
          rows="3"
          hint="A brief summary of the artifact content"
        />
      </v-col>
    </v-row>
    <custom-field-input v-if="isFMEA" v-model="artifact" />
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactModel, DocumentType, SelectOption } from "@/types";
import { documentTypeMap, logicTypeOptions, safetyCaseOptions } from "@/util";
import { documentModule, projectModule } from "@/store";
import { typeOptionsStore } from "@/hooks";
import { getDoesArtifactExist } from "@/api";
import {
  ArtifactInput,
  CustomFieldInput,
  Typography,
} from "@/components/common";

/**
 * Inputs for artifact creation.
 *
 * @emits-1 `change:parent` (string) - Called with the parent id when the parent input changes.
 * @emits-2 `change:valid` (boolean) - Called with weather the name is currently valid.
 */
export default Vue.extend({
  name: "ArtifactCreator",
  components: { CustomFieldInput, ArtifactInput, Typography },
  props: {
    artifact: {
      type: Object as PropType<ArtifactModel>,
      required: true,
    },
    currentArtifactName: String,
    isEditMode: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      parentId: "",

      isNameValid: !!this.artifact?.name,
      nameError: "",
      nameCheckTimer: undefined as ReturnType<typeof setTimeout> | undefined,
      nameCheckIsLoading: false,

      safetyCaseTypes: safetyCaseOptions(),
      logicTypes: logicTypeOptions(),
    };
  },
  computed: {
    /**
     * @return The artifact name.
     */
    name(): string {
      return this.artifact.name;
    },
    /**
     * @return Whether the artifact type is for an FTA node.
     */
    isFTA(): boolean {
      return this.artifact.documentType === DocumentType.FTA;
    },
    /**
     * @return Whether the artifact type is for a safety case node.
     */
    isSafetyCase(): boolean {
      return this.artifact.documentType === DocumentType.SAFETY_CASE;
    },
    /**
     * @return Whether the artifact type is for an FMEA node.
     */
    isFMEA(): boolean {
      return this.artifact.documentType === DocumentType.FMEA;
    },
    /**
     * @return The document types allowed on the current document.
     */
    documentTypes(): SelectOption[] {
      return documentTypeMap()[documentModule.type];
    },
    /**
     * @return The types of artifacts that exist so far.
     */
    artifactTypes(): string[] {
      return typeOptionsStore.artifactTypes;
    },
  },
  watch: {
    /**
     * Checks for name conflicts when the name changes.
     */
    name(newName: string): void {
      if (this.nameCheckTimer) {
        clearTimeout(this.nameCheckTimer);
      }

      this.nameCheckIsLoading = true;
      this.isNameValid = false;
      this.nameCheckTimer = setTimeout(() => {
        if (!newName) {
          this.isNameValid = false;
          this.nameCheckIsLoading = false;
        } else if (newName === this.currentArtifactName) {
          this.isNameValid = true;
          this.nameCheckIsLoading = false;
        } else {
          getDoesArtifactExist(projectModule.versionId, newName).then(
            (nameExists) => {
              this.nameCheckIsLoading = false;
              this.isNameValid = !nameExists;
              this.nameError = this.isNameValid
                ? ""
                : "Name is already used, please select another.";
            }
          );
        }
      }, 500);
    },
    /**
     * Emits changes to the parent node ID.
     */
    parentId(newId: string): void {
      this.$emit("change:parent", newId);
    },
    /**
     * Emits changes to the valid status.
     */
    isNameValid(isValid: boolean): void {
      this.$emit("change:valid", isValid);
    },
  },
});
</script>
