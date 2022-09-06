<template>
  <generic-modal
    :title="creatorTitle"
    :isOpen="!!isOpen"
    :isLoading="isLoading"
    size="l"
    data-cy="modal-artifact-save"
    @close="handleClose"
  >
    <template v-slot:body>
      <artifact-creator-inputs
        :artifact="editedArtifact"
        :current-artifact-name="currentArtifactName"
        :is-edit-mode="!!artifact"
        @change:parent="parentId = $event"
        @change:documentType="handleDocumentTypeChange"
        @change:valid="isNameValid = $event"
      />
    </template>
    <template v-slot:actions>
      <v-row justify="end">
        <v-btn
          color="primary"
          :disabled="!canSave"
          data-cy="button-artifact-save"
          @click="handleSubmit"
        >
          Save
        </v-btn>
      </v-row>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactModel, DocumentType } from "@/types";
import { createArtifact, createArtifactOfType } from "@/util";
import {
  appStore,
  artifactStore,
  documentStore,
  selectionStore,
} from "@/hooks";
import { handleSaveArtifact } from "@/api";
import { GenericModal } from "@/components/common";
import ArtifactCreatorInputs from "./ArtifactCreatorInputs.vue";

/**
 * Modal for artifact creation.
 */
export default Vue.extend({
  name: "ArtifactCreator",
  components: {
    GenericModal,
    ArtifactCreatorInputs,
  },
  data() {
    return {
      editedArtifact: createArtifact(selectionStore.selectedArtifact),
      parentId: "",
      isNameValid: false,
      isLoading: false,
      canSave: false,
    };
  },
  computed: {
    /**
     * @return The selected artifact.
     */
    artifact(): ArtifactModel | undefined {
      return selectionStore.selectedArtifact;
    },
    /**
     * Returns whether the artifact creator is open.
     */
    isOpen(): string | boolean {
      return appStore.isArtifactCreatorOpen;
    },
    /**
     * @return The selected artifact.
     */
    creatorTitle(): string {
      return this.artifact ? "Edit Artifact" : "Create Artifact";
    },
    currentArtifactName(): string {
      return this.artifact?.name || "";
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
     * @return The parent artifact of a logic node.
     */
    parentArtifact(): ArtifactModel | undefined {
      return this.parentId
        ? artifactStore.getArtifactById(this.parentId)
        : undefined;
    },
    /**
     * @return The computed type based on the artifact's document type.
     */
    computedArtifactType(): string {
      if (this.isFTA) {
        return this.parentArtifact?.type || this.editedArtifact.type;
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
      this.isNameValid = !!this.artifact?.name;
      this.canSave = this.isValid;
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
    /**
     * Checks whether the artifact is valid when it changes.
     */
    parentId() {
      this.canSave = this.isValid;
    },
    /**
     * Checks whether the artifact is valid when it changes.
     */
    isNameValid() {
      this.canSave = this.isValid;
    },
  },
  methods: {
    /**
     * Updates artifact fields when the document type changes.
     */
    handleDocumentTypeChange(): void {
      this.editedArtifact = createArtifactOfType(
        this.artifact,
        this.artifact?.type
      );
    },
    /**
     * Attempts to save the artifact.
     */
    handleSubmit(): void {
      const { documentId } = documentStore.currentDocument;
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

      handleSaveArtifact(artifact, isUpdate, this.parentArtifact, {
        onSuccess: () => {
          this.isLoading = false;
          this.handleClose();
        },
        onError: () => (this.isLoading = false),
      });
    },
    /**
     * Closes the artifact creator.
     */
    handleClose(): void {
      appStore.closeArtifactCreator();
    },
  },
});
</script>
