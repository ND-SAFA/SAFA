<template>
  <GenericModal
    title="Create New Artifact"
    :isOpen="isOpen"
    :isLoading="isLoading"
    @onClose="$emit('onClose')"
  >
    <template v-slot:body>
      <v-container>
        <v-row justify="center">
          <v-col cols="6">
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
            <v-text-field label="Artifact Summary" v-model="summary" />
            <v-text-field label="Artifact Body" v-model="body" />
          </v-col>
        </v-row>
      </v-container>
    </template>
    <template v-slot:actions>
      <v-row justify="center">
        <v-btn color="primary" :disabled="!isValid" @click="onSubmit">
          <v-icon>mdi-content-save</v-icon>
        </v-btn>
      </v-row>
    </template>
  </GenericModal>
</template>
<script lang="ts">
import Vue from "vue";
import { createNewArtifact, isArtifactNameTaken } from "@/api/artifact-api";
import GenericModal from "@/components/common/generic/GenericModal.vue";
import { Artifact } from "@/types";
import ButtonRow from "@/components/common/button-row/ButtonRow.vue";
import { ButtonDefinition, ButtonType, ListMenuDefinition } from "@/types";
import { appModule, projectModule } from "@/store";
const DEFAULT_NAME_HINT = "Please select an identifier for the artifact";

export default Vue.extend({
  components: { GenericModal, ButtonRow },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      name: "",
      summary: "",
      body: "",
      isLoading: false,
      isValid: false,
      isNameValid: false,
      nameHint: DEFAULT_NAME_HINT,
      nameError: "",
      buttonDefinitions: [] as ButtonDefinition[],
      type: "",
    };
  },
  computed: {
    aggregate(): string {
      return this.name + this.summary + this.body + this.type;
    },

    projectId(): string {
      return projectModule.getProject.projectId;
    },
    versionId(): string | undefined {
      return projectModule.getProject.projectVersion?.versionId;
    },
    artifactTypes(): string[] {
      return projectModule.getArtifactTypes;
    },
  },
  watch: {
    artifactTypes(): void {
      this.setButtonDefinitions();
    },
    isOpen(isOpen: boolean): void {
      if (isOpen) {
        this.setButtonDefinitions();
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
    aggregate(): void {
      if (this.isNameValid && this.body !== "" && this.type !== "") {
        this.isValid = true;
      } else {
        this.isValid = false;
      }
    },
  },
  methods: {
    setButtonDefinitions(): void {
      const menuItem: ListMenuDefinition = {
        type: ButtonType.LIST_MENU,
        label: "Artifact Type",
        menuItems: this.artifactTypes,
        menuHandlers: this.artifactTypes.map(
          (type) => () => (this.type = type)
        ),
        buttonColor: "primary",
        buttonIsText: false,
        showSelectedValue: true,
      };
      this.buttonDefinitions = [menuItem];
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
      createNewArtifact(this.versionId, artifact)
        .then(() => {
          this.$emit("onClose");
        })
        .catch((e) => console.error(e))
        .finally(() => (this.isLoading = false));
    },
  },
});
</script>
