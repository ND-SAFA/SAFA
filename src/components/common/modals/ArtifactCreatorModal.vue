<template>
  <generic-modal
    :title="title"
    :isOpen="isOpen"
    :isLoading="isLoading"
    @close="$emit('onClose')"
  >
    <template v-slot:body>
      <v-container>
        <v-text-field
          v-model="name"
          outlined
          dense
          rounded
          label="Artifact Id"
          color="primary"
          :hint="nameHint"
          :error-messages="nameError"
        />
        <button-row :definitions="buttonDefinitions" justify="center" />
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
import { ButtonDefinition, ButtonType, Artifact } from "@/types";
import { createOrUpdateArtifactHandler, isArtifactNameTaken } from "@/api";
import { appModule, projectModule } from "@/store";
import { GenericModal } from "@/components/common/generic";
import { ButtonRow } from "@/components/common/button-row";

const DEFAULT_NAME_HINT = "Please select an identifier for the artifact";

export default Vue.extend({
  components: { GenericModal, ButtonRow },
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
    };
  },
  computed: {
    projectId(): string {
      return projectModule.getProject.projectId;
    },
    versionId(): string | undefined {
      return projectModule.getProject.projectVersion?.versionId;
    },
    artifactTypes(): string[] {
      return projectModule.getArtifactTypes;
    },
    isValid(): boolean {
      return this.isNameValid && this.body !== "" && this.type !== "";
    },
  },
  watch: {
    artifactTypes(): void {
      this.setButtonDefinitions();
    },
    isOpen(isOpen: boolean): void {
      if (isOpen) {
        this.setButtonDefinitions();
      } else {
        this.name = this.artifact?.name || "";
        this.summary = this.artifact?.summary || "";
        this.body = this.artifact?.body || "";
        this.type = this.artifact?.type || "";
      }
    },
    name(newName: string): void {
      isArtifactNameTaken(this.projectId, newName).then((res) => {
        this.isNameValid = !res.artifactExists;

        if (this.isNameValid) {
          this.nameError = "";
        } else {
          this.nameError = "Name is already used, please select another.";
        }
      });
    },
  },
  methods: {
    setButtonDefinitions(): void {
      this.buttonDefinitions = [
        {
          type: ButtonType.LIST_MENU,
          label: this.type || "Artifact Type",
          menuItems: this.artifactTypes,
          menuHandlers: this.artifactTypes.map(
            (type) => () => (this.type = type)
          ),
          buttonColor: "primary",
          buttonIsText: false,
          showSelectedValue: true,
        },
      ];
    },
    onSubmit(): void {
      // only called when isValid / button is enabled
      const artifact: Artifact = {
        name: this.name,
        type: this.type,
        summary: this.summary,
        body: this.body,
      };

      this.isLoading = true;

      if (this.versionId === undefined) {
        appModule.onWarning("Please select a project version.");
        return;
      }

      createOrUpdateArtifactHandler(this.versionId, artifact)
        .then(() => {
          this.$emit("onClose");
        })
        .catch(() => appModule.onWarning("Unable to create artifact."))
        .finally(() => (this.isLoading = false));
    },
  },
});
</script>
