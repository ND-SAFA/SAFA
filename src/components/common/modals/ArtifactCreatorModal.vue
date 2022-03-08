<template>
  <generic-modal
    :title="title"
    :isOpen="isOpen"
    :isLoading="isLoading"
    @close="$emit('close')"
  >
    <template v-slot:body>
      <v-container>
        <v-text-field
          filled
          v-model="name"
          label="Artifact Name"
          color="primary"
          hint="Please select an identifier for the artifact"
          :error-messages="nameError"
          :loading="nameCheckIsLoading"
        />
        <v-combobox
          filled
          v-if="!isFTA && !isSafetyCase"
          v-model="artifactType"
          :items="artifactTypes"
          label="Artifact Type"
        />
        <v-select
          filled
          label="Document Type"
          v-model="documentType"
          :items="documentTypes"
          item-text="name"
          item-value="id"
        />
        <v-select
          v-if="isFTA"
          filled
          label="Logic Type"
          v-model="logicType"
          :items="logicTypes"
        />
        <artifact-input
          v-if="isFTA"
          v-model="parentId"
          :multiple="false"
          label="Parent Artifact"
        />
        <v-select
          v-if="isSafetyCase"
          filled
          label="Safety Case Type"
          v-model="safetyCaseType"
          :items="safetyCaseTypes"
          item-text="name"
          item-value="id"
        />
        <v-textarea
          v-if="!isFTA"
          filled
          label="Artifact Summary"
          v-model="summary"
          class="mt-3"
          rows="3"
        />
        <v-textarea
          filled
          v-if="!isFTA"
          label="Artifact Body"
          v-model="body"
          rows="3"
        />
      </v-container>
    </template>
    <template v-slot:actions>
      <v-row justify="end">
        <v-btn color="primary" :disabled="!isValid" @click="onSubmit">
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
  ButtonDefinition,
  DocumentType,
  FTANodeType,
  SafetyCaseType,
  SelectOption,
} from "@/types";
import { documentTypeOptions, safetyCaseOptions } from "@/util";
import { createOrUpdateArtifactHandler, isArtifactNameTaken } from "@/api";
import {
  artifactModule,
  documentModule,
  logModule,
  projectModule,
  typeOptionsModule,
} from "@/store";
import { ArtifactInput } from "@/components/common/index";
import { GenericModal } from "@/components/common/generic";
import { setTimeout } from "timers";

/**
 * Modal for artifact creation.
 *
 * @emits `close` - Emitted when modal is exited or artifact is created.
 */
export default Vue.extend({
  components: { GenericModal, ArtifactInput },
  props: {
    title: {
      type: String,
      default: "Create New Artifact",
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
    artifact: {
      type: Object as PropType<Artifact>,
      required: false,
    },
  },
  data() {
    return {
      name: this.artifact?.name || "",
      summary: this.artifact?.summary || "",
      body: this.artifact?.body || "",
      artifactType: this.artifact?.type || "",
      documentType: this.artifact?.documentType || DocumentType.ARTIFACT_TREE,
      safetyCaseType: this.artifact?.safetyCaseType || SafetyCaseType.GOAL,
      logicType: this.artifact?.logicType || FTANodeType.AND,

      parentId: "",

      isLoading: false,
      isNameValid: !!this.artifact?.name,
      nameError: "",
      buttonDefinitions: [] as ButtonDefinition[],
      nameCheckTimer: undefined as ReturnType<typeof setTimeout> | undefined,
      nameCheckIsLoading: false,
    };
  },
  computed: {
    projectId(): string {
      return projectModule.projectId;
    },
    versionId(): string {
      return projectModule.versionIdWithLog || "";
    },

    isFTA(): boolean {
      return this.documentType === DocumentType.FTA;
    },
    isSafetyCase(): boolean {
      return this.documentType === DocumentType.SAFETY_CASE;
    },
    isValid(): boolean {
      const isValidArtifact = this.isNameValid && this.body;
      const isValidFTA = this.isFTA
        ? this.logicType && this.parentId
        : this.artifactType;
      const isValidSC = this.isSafetyCase
        ? this.safetyCaseType
        : this.artifactType;

      return !!(isValidArtifact && isValidFTA && isValidSC);
    },

    documentTypes(): SelectOption[] {
      const documentType = documentModule.document.type;
      const options = documentTypeOptions();

      if (documentType === DocumentType.FTA) {
        return options.filter(({ id }) => id !== DocumentType.SAFETY_CASE);
      } else if (documentType === DocumentType.SAFETY_CASE) {
        return options.filter(({ id }) => id !== DocumentType.FTA);
      } else {
        return options.filter(({ id }) => id == DocumentType.ARTIFACT_TREE);
      }
    },
    safetyCaseTypes: safetyCaseOptions,
    artifactTypes(): string[] {
      return typeOptionsModule.artifactTypes;
    },
    logicTypes(): FTANodeType[] {
      return [FTANodeType.AND, FTANodeType.OR];
    },

    parentArtifact(): Artifact | undefined {
      return this.parentId
        ? artifactModule.getArtifactById(this.parentId)
        : undefined;
    },
    computedArtifactType(): string {
      if (this.isFTA) {
        return this.parentArtifact?.type || this.artifactType;
      } else if (this.isSafetyCase) {
        return this.safetyCaseType;
      } else {
        return this.artifactType;
      }
    },
    computedName(): string {
      return this.isFTA ? `${this.parentId}-logic` : this.name;
    },
  },
  watch: {
    isOpen(isOpen: boolean): void {
      if (!isOpen) {
        this.name = this.artifact?.name || "";
        this.summary = this.artifact?.summary || "";
        this.body = this.artifact?.body || "";
        this.artifactType = this.artifact?.type || "";
        this.documentType =
          this.artifact?.documentType || DocumentType.ARTIFACT_TREE;
        this.logicType = this.artifact?.logicType || FTANodeType.AND;
        this.safetyCaseType =
          this.artifact?.safetyCaseType || SafetyCaseType.GOAL;
        this.parentId = "";
      }
    },
    name(newName: string): void {
      if (newName !== "") {
        if (this.nameCheckTimer) {
          clearTimeout(this.nameCheckTimer);
        }

        this.nameCheckIsLoading = true;
        this.nameCheckTimer = setTimeout(() => {
          if (!this.versionId) return;

          isArtifactNameTaken(this.versionId, newName).then((res) => {
            this.nameCheckIsLoading = false;
            this.isNameValid = !res.artifactExists;

            if (this.isNameValid) {
              this.nameError = "";
            } else {
              this.nameError = "Name is already used, please select another.";
            }
          });
        }, 500);
      }
    },
  },
  methods: {
    onSubmit(): void {
      const { documentId } = documentModule.document;
      const isUpdate = this.artifact !== undefined;
      const artifact: Artifact = {
        id: this.artifact?.id || "",
        name: this.computedName,
        type: this.computedArtifactType,
        summary: this.summary,
        body: this.body,
        documentType: this.documentType,
        documentIds: documentId ? [documentId] : [],
        logicType: this.isFTA ? this.logicType : undefined,
        safetyCaseType: this.isSafetyCase ? this.safetyCaseType : undefined,
      };

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
