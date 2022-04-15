<template>
  <generic-modal
    :title="title"
    :isOpen="!!isOpen"
    :isLoading="isLoading"
    @close="$emit('close')"
  >
    <template v-slot:body>
      <v-container>
        <v-select
          filled
          label="Document Type"
          v-model="editedArtifact.documentType"
          :items="documentTypes"
          item-text="name"
          item-value="id"
        />
        <v-text-field
          filled
          v-if="!isFTA"
          v-model="editedArtifact.name"
          label="Artifact Name"
          color="primary"
          hint="Please select an identifier for the artifact"
          :error-messages="nameError"
          :loading="nameCheckIsLoading"
        />
        <v-combobox
          filled
          v-if="!isFTA && !isSafetyCase && !isFMEA"
          v-model="editedArtifact.type"
          :items="artifactTypes"
          label="Artifact Type"
        />
        <v-select
          filled
          v-if="isFTA"
          label="Logic Type"
          v-model="editedArtifact.logicType"
          :items="logicTypes"
          item-text="name"
          item-value="id"
        />
        <artifact-input
          only-document-artifacts
          v-if="isFTA"
          v-model="parentId"
          :multiple="false"
          label="Parent Artifact"
        />
        <v-select
          filled
          v-if="isSafetyCase"
          label="Safety Case Type"
          v-model="editedArtifact.safetyCaseType"
          :items="safetyCaseTypes"
          item-text="name"
          item-value="id"
        />
        <v-textarea
          filled
          v-if="!isFTA"
          label="Artifact Summary"
          v-model="editedArtifact.summary"
          rows="3"
        />
        <v-textarea
          filled
          v-if="!isFTA"
          label="Artifact Body"
          v-model="editedArtifact.body"
          rows="3"
        />
        <custom-field-input v-if="isFMEA" v-model="editedArtifact" />
      </v-container>
    </template>
    <template v-slot:actions>
      <v-row justify="end">
        <v-btn color="primary" :disabled="!canSave" @click="onSubmit">
          Save
        </v-btn>
      </v-row>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { setTimeout } from "timers";
import { Artifact, DocumentType, SelectOption } from "@/types";
import {
  createArtifact,
  createArtifactOfType,
  documentTypeMap,
  logicTypeOptions,
  safetyCaseOptions,
} from "@/util";
import {
  artifactModule,
  documentModule,
  projectModule,
  typeOptionsModule,
} from "@/store";
import { handleSaveArtifact, getDoesArtifactExist } from "@/api";
import {
  ArtifactInput,
  GenericModal,
  CustomFieldInput,
} from "@/components/common";

/**
 * Modal for artifact creation.
 *
 * @emits `close` - Emitted when modal is exited or artifact is created.
 */
export default Vue.extend({
  name: "ArtifactCreator",
  components: { CustomFieldInput, GenericModal, ArtifactInput },
  props: {
    title: {
      type: String,
      default: "Create New Artifact",
    },
    isOpen: {
      type: [Boolean, String],
      required: true,
    },
    artifact: {
      type: Object as PropType<Artifact>,
      required: false,
    },
  },
  data() {
    return {
      editedArtifact: createArtifact(this.artifact),
      parentId: "",
      isLoading: false,
      isNameValid: !!this.artifact?.name,
      nameError: "",
      nameCheckTimer: undefined as ReturnType<typeof setTimeout> | undefined,
      nameCheckIsLoading: false,
      canSave: false,
      safetyCaseTypes: safetyCaseOptions(),
      logicTypes: logicTypeOptions(),
    };
  },
  computed: {
    /**
     * @return The artifact name.
     */
    name(): string {
      return this.editedArtifact.name;
    },
    /**
     * @return Whether the artifact type is for an FTA node.
     */
    isFTA(): boolean {
      return this.editedArtifact.documentType === DocumentType.FTA;
    },
    /**
     * @return Whether the artifact type is for a safety case node.
     */
    isSafetyCase(): boolean {
      return this.editedArtifact.documentType === DocumentType.SAFETY_CASE;
    },
    /**
     * @return Whether the artifact type is for an FMEA node.
     */
    isFMEA(): boolean {
      return this.editedArtifact.documentType === DocumentType.FMEA;
    },
    /**
     * @return Whether the artifact data is valid.
     */
    isValid(): boolean {
      const { logicType, safetyCaseType, type, body } = this.editedArtifact;

      if (this.isFTA) {
        return !!(logicType && this.parentId);
      } else if (this.isSafetyCase) {
        return !!(this.isNameValid && body && safetyCaseType);
      } else if (this.isFMEA) {
        return !!(this.isNameValid && body);
      } else {
        return !!(this.isNameValid && body && type);
      }
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
      return typeOptionsModule.artifactTypes;
    },
    /**
     * @return The parent artifact of a logic node.
     */
    parentArtifact(): Artifact | undefined {
      return this.isFTA && this.parentId
        ? artifactModule.getArtifactById(this.parentId)
        : undefined;
    },
    /**
     * @return The computed type based on the artifact's document type.
     */
    computedArtifactType(): string {
      if (this.isFTA) {
        return this.parentArtifact?.type || this.editedArtifact.type;
      } else if (this.isSafetyCase) {
        return this.editedArtifact.safetyCaseType || "";
      } else if (this.isFMEA) {
        return "FMEA";
      } else {
        return this.editedArtifact.type;
      }
    },
    /**
     * @return The computed name based on the artifact's document type.
     */
    computedName(): string {
      const { name, logicType } = this.editedArtifact;

      return this.isFTA
        ? `${this.parentArtifact?.name || this.parentId}-${logicType}`
        : name;
    },
  },
  watch: {
    /**
     * Resets artifact data when opened.
     * If opened with a string, attempts to switch the artifact type to match the type given.
     */
    isOpen(openOrType: boolean | string): void {
      if (!openOrType) return;

      this.editedArtifact = createArtifactOfType(this.artifact, openOrType);
    },
    /**
     * Checks for name conflicts when the name changes.
     */
    name(newName: string): void {
      if (this.nameCheckTimer) {
        clearTimeout(this.nameCheckTimer);
      }

      this.nameCheckIsLoading = true;
      this.nameCheckTimer = setTimeout(() => {
        if (!newName) {
          this.isNameValid = this.canSave = false;
          this.nameCheckIsLoading = false;
        } else if (newName === this.artifact?.name) {
          this.isNameValid = this.canSave = true;
          this.nameCheckIsLoading = false;
        } else {
          getDoesArtifactExist(projectModule.versionId, newName).then(
            (nameExists) => {
              this.nameCheckIsLoading = false;
              this.canSave = this.isNameValid = !nameExists;
              this.nameError = this.isNameValid
                ? ""
                : "Name is already used, please select another.";
            }
          );
        }
      }, 500);
    },
    /**
     * Checks whether the artifact is valid when it changes.
     */
    editedArtifact: {
      handler(): void {
        this.canSave = this.isValid;
      },
      deep: true,
    },
  },
  methods: {
    /**
     * Attempts to save the artifact.
     */
    onSubmit(): void {
      const { documentId } = documentModule.document;
      const { logicType, safetyCaseType } = this.editedArtifact;
      const isUpdate = this.artifact !== undefined;
      const artifact = createArtifact({
        ...this.editedArtifact,
        name: this.computedName,
        type: this.computedArtifactType,
        documentIds: documentId ? [documentId] : [],
        logicType: this.isFTA ? logicType : undefined,
        safetyCaseType: this.isSafetyCase ? safetyCaseType : undefined,
      });

      this.isLoading = true;

      handleSaveArtifact(artifact, isUpdate, this.parentArtifact, () =>
        this.$emit("close")
      ).then(() => (this.isLoading = false));
    },
  },
});
</script>
