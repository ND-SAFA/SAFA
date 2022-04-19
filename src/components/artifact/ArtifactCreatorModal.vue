<template>
  <generic-modal
    :title="title"
    :isOpen="!!isOpen"
    :isLoading="isLoading"
    @close="$emit('close')"
  >
    <template v-slot:body>
      <artifact-creator-inputs
        :artifact="editedArtifact"
        :current-artifact-name="currentArtifactName"
        @change:parent="parentId = $event"
        @change:valid="isNameValid = $event"
      />
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
import { Artifact, DocumentType } from "@/types";
import { createArtifact, createArtifactOfType } from "@/util";
import { artifactModule, documentModule } from "@/store";
import { handleSaveArtifact } from "@/api";
import { GenericModal } from "@/components/common";
import ArtifactCreatorInputs from "./ArtifactCreatorInputs.vue";

/**
 * Modal for artifact creation.
 *
 * @emits `close` - Emitted when modal is exited or artifact is created.
 */
export default Vue.extend({
  name: "ArtifactCreator",
  components: {
    GenericModal,
    ArtifactCreatorInputs,
  },
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
      isNameValid: !!this.artifact?.name,
      isLoading: false,
      canSave: false,
    };
  },
  computed: {
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

      handleSaveArtifact(artifact, isUpdate, this.parentArtifact, {
        onSuccess: () => {
          this.$emit("close");
          this.isLoading = false;
        },
        onError: () => (this.isLoading = false),
      });
    },
  },
});
</script>
