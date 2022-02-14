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
          label="Artifact Id"
          color="primary"
          :hint="nameHint"
          :error-messages="nameError"
          :loading="nameCheckIsLoading"
        />
        <v-combobox
          filled
          v-model="type"
          :items="artifactTypes"
          label="Artifact Type"
        />
        <v-textarea
          filled
          label="Artifact Summary"
          v-model="summary"
          class="mt-3"
          rows="3"
        />
        <v-textarea filled label="Artifact Body" v-model="body" rows="3" />
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
import { ButtonDefinition, Artifact } from "@/types";
import { createOrUpdateArtifactHandler, isArtifactNameTaken } from "@/api";
import {
  typeOptionsModule,
  logModule,
  projectModule,
  documentModule,
} from "@/store";
import { GenericModal } from "@/components/common/generic";

const DEFAULT_NAME_HINT = "Please select an identifier for the artifact";

/**
 * Modal for artifact creation.
 *
 * @emits `close` - Emitted when modal is exited or artifact is created.
 */
export default Vue.extend({
  components: { GenericModal },
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
      type: this.artifact?.type || "",
      isLoading: false,
      isNameValid: !!this.artifact?.name,
      nameHint: DEFAULT_NAME_HINT,
      nameError: "",
      buttonDefinitions: [] as ButtonDefinition[],
      nameCheckTimer: undefined as NodeJS.Timeout | undefined,
      nameCheckIsLoading: false,
    };
  },
  computed: {
    projectId(): string {
      return projectModule.projectId;
    },
    versionId(): string | undefined {
      return projectModule.versionIdWithLog;
    },
    artifactTypes(): string[] {
      return typeOptionsModule.artifactTypes;
    },
    isValid(): boolean {
      return this.isNameValid && this.body !== "" && this.type !== "";
    },
  },
  watch: {
    isOpen(isOpen: boolean): void {
      if (!isOpen) {
        this.name = this.artifact?.name || "";
        this.summary = this.artifact?.summary || "";
        this.body = this.artifact?.body || "";
        this.type = this.artifact?.type || "";
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
      const versionId = this.versionId;
      const { documentId } = documentModule.document;
      const artifact: Artifact = {
        id: this.artifact?.id || "",
        name: this.name,
        type: this.type,
        summary: this.summary,
        body: this.body,
        documentIds: documentId ? [documentId] : [],
      };

      if (!versionId) return;

      this.isLoading = true;

      const isUpdate = this.artifact !== undefined;

      console.log(documentModule.document, artifact);

      createOrUpdateArtifactHandler(versionId, artifact, isUpdate)
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
