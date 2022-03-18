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
          v-if="!isFTA"
          filled
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
          v-if="isFTA"
          filled
          label="Logic Type"
          v-model="editedArtifact.logicType"
          :items="logicTypes"
        />
        <artifact-input
          only-document-artifacts
          v-if="isFTA"
          v-model="parentId"
          :multiple="false"
          label="Parent Artifact"
        />
        <v-select
          v-if="isSafetyCase"
          filled
          label="Safety Case Type"
          v-model="editedArtifact.safetyCaseType"
          :items="safetyCaseTypes"
          item-text="name"
          item-value="id"
        />
        <v-textarea
          v-if="!isFTA"
          filled
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
          <v-icon>mdi-content-save</v-icon>
          <span class="ml-1">Save</span>
        </v-btn>
      </v-row>
    </template>
  </generic-modal>
</template>
<script lang="ts">
import Vue, { PropType } from "vue";
import {
  Artifact,
  DocumentType,
  FTANodeType,
  SafetyCaseType,
  SelectOption,
} from "@/types";
import {
  createArtifact,
  documentTypeMap,
  logicTypeOptions,
  safetyCaseOptions,
} from "@/util";
import { createOrUpdateArtifactHandler, isArtifactNameTaken } from "@/api";
import {
  artifactModule,
  documentModule,
  logModule,
  projectModule,
  typeOptionsModule,
} from "@/store";
import {
  ArtifactInput,
  GenericModal,
  CustomFieldInput,
} from "@/components/common";
import { setTimeout } from "timers";

/**
 * Modal for artifact creation.
 *
 * @emits `close` - Emitted when modal is exited or artifact is created.
 */
export default Vue.extend({
  name: "artifact-creator",
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
    };
  },
  computed: {
    name(): string {
      return this.editedArtifact.name;
    },

    projectId(): string {
      return projectModule.projectId;
    },
    versionId(): string {
      return projectModule.versionIdWithLog || "";
    },

    isFTA(): boolean {
      return this.editedArtifact.documentType === DocumentType.FTA;
    },
    isSafetyCase(): boolean {
      return this.editedArtifact.documentType === DocumentType.SAFETY_CASE;
    },
    isFMEA(): boolean {
      return this.editedArtifact.documentType === DocumentType.FMEA;
    },
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

    safetyCaseTypes: safetyCaseOptions,
    logicTypes: logicTypeOptions,
    documentTypes(): SelectOption[] {
      return documentTypeMap()[documentModule.type];
    },
    artifactTypes(): string[] {
      return typeOptionsModule.artifactTypes;
    },

    parentArtifact(): Artifact | undefined {
      return this.parentId
        ? artifactModule.getArtifactById(this.parentId)
        : undefined;
    },
    computedArtifactType(): string {
      if (this.isFTA) {
        return this.parentArtifact?.type || this.editedArtifact.type;
      } else if (this.isSafetyCase) {
        return this.editedArtifact.safetyCaseType || "";
      } else {
        return this.editedArtifact.type;
      }
    },
    computedName(): string {
      const { name, logicType } = this.editedArtifact;

      return this.isFTA
        ? `${this.parentArtifact?.name || this.parentId}-${logicType}`
        : name;
    },
  },
  watch: {
    isOpen(isOpen: boolean | string): void {
      if (isOpen === true) {
        this.editedArtifact = createArtifact(this.artifact);
        this.parentId = "";
      } else if (typeof isOpen === "string") {
        if (isOpen in FTANodeType) {
          this.editedArtifact = createArtifact({
            documentType: DocumentType.FTA,
            logicType: isOpen as FTANodeType,
          });
        } else if (isOpen in SafetyCaseType) {
          this.editedArtifact = createArtifact({
            documentType: DocumentType.SAFETY_CASE,
            safetyCaseType: isOpen as SafetyCaseType,
          });
        }
      }
    },
    name(newName: string): void {
      if (!newName) return;

      if (this.nameCheckTimer) {
        clearTimeout(this.nameCheckTimer);
      }

      this.nameCheckIsLoading = true;
      this.nameCheckTimer = setTimeout(() => {
        isArtifactNameTaken(this.versionId, newName).then((res) => {
          this.nameCheckIsLoading = false;
          this.isNameValid =
            !res.artifactExists || newName === this.artifact.name;
          this.nameError = this.isNameValid
            ? ""
            : "Name is already used, please select another.";
          this.canSave = this.isNameValid;
        });
      }, 500);
    },
    editedArtifact: {
      handler(): void {
        this.canSave = this.isValid;
      },
      deep: true,
    },
  },
  methods: {
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

      createOrUpdateArtifactHandler(
        this.versionId,
        artifact,
        isUpdate,
        this.parentArtifact
      )
        .then(async () => {
          this.$emit("close");
        })
        .catch((e) => {
          logModule.onDevError(e);
          logModule.onWarning("Unable to create artifact.");
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
});
</script>
