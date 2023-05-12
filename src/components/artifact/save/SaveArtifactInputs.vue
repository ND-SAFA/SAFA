<template>
  <div>
    <text-input
      v-if="!store.isFTA"
      v-model="store.editedArtifact.name"
      label="Artifact Name"
      hint="Please select an identifier for the artifact"
      :error-message="nameError"
      :loading="nameCheckLoading"
      class="q-mb-md"
      data-cy="input-artifact-name"
    />
    <artifact-type-input
      v-if="!store.isFTA && !store.isSafetyCase && !store.isFMEA"
      v-model="store.editedArtifact.type"
      label="Artifact Type"
      hint="Required"
      class="q-mb-md"
      data-cy="input-artifact-type"
    />

    <text-input
      v-if="!store.isFTA"
      v-model="store.editedArtifact.body"
      label="Artifact Body"
      type="textarea"
      hint="Required"
      class="q-mb-md"
      data-cy="input-artifact-body"
    >
      <template #append>
        <icon-button
          :loading="promptLoading"
          tooltip="Generate the body based on a prompt"
          icon="generate"
          @click="handleGenerateBody"
        />
      </template>
    </text-input>

    <text-input
      v-if="!store.isFTA && !!store.hasSummary"
      v-model="store.editedArtifact.summary"
      label="Artifact Summary"
      type="textarea"
      class="q-mb-md"
      data-cy="input-artifact-summary"
    />

    <select-input
      v-if="showDocumentType"
      v-model="store.editedArtifact.documentType"
      label="Document Type"
      :options="documentTypes"
      option-label="name"
      option-value="id"
      option-to-value
      hint="Which type of document this artifact belongs to"
      class="q-mb-md"
      data-cy="input-artifact-document"
    />
    <select-input
      v-if="store.isSafetyCase"
      v-model="store.editedArtifact.safetyCaseType"
      label="Safety Case Type"
      :options="safetyCaseTypes"
      option-label="name"
      option-value="id"
      option-to-value
      class="q-mb-md"
      data-cy="input-artifact-sc"
    />
    <select-input
      v-if="store.isFTA"
      v-model="store.editedArtifact.logicType"
      label="Logic Type"
      :options="logicTypes"
      option-label="name"
      option-value="id"
      option-to-value
      class="q-mb-md"
      data-cy="input-artifact-logic"
    />
    <artifact-input
      v-if="!store.isUpdate"
      v-model="store.parentId"
      only-document-artifacts
      label="Parent Artifact"
      data-cy="input-artifact-parent"
      class="q-mb-md"
    />

    <attribute-list-input :artifact="store.editedArtifact" />
  </div>
</template>

<script lang="ts">
/**
 * Inputs for artifact creation and editing.
 */
export default {
  name: "SaveArtifactInputs",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { documentTypeMap, logicTypeOptions, safetyCaseOptions } from "@/util";
import { artifactSaveStore, documentStore, projectStore } from "@/hooks";
import {
  createPrompt,
  getDoesArtifactExist,
  handleGenerateArtifactBody,
} from "@/api";
import {
  ArtifactInput,
  ArtifactTypeInput,
  AttributeListInput,
  TextInput,
  SelectInput,
} from "@/components/common";
import IconButton from "@/components/common/button/IconButton.vue";

const safetyCaseTypes = safetyCaseOptions();
const logicTypes = logicTypeOptions();

const nameCheckTimer = ref<ReturnType<typeof setTimeout> | undefined>();
const nameCheckLoading = ref(false);
const promptLoading = ref(false);

const store = computed(() => artifactSaveStore);

const documentTypes = computed(
  () => documentTypeMap()[documentStore.currentType]
);

const showDocumentType = computed(() => documentTypes.value.length > 1);

const nameError = computed(() =>
  nameCheckLoading.value ? false : artifactSaveStore.nameError
);

/**
 * Generates the body of the artifact based on a prompt.
 */
function handleGenerateBody() {
  promptLoading.value = true;

  handleGenerateArtifactBody({
    onComplete: () => (promptLoading.value = false),
  });
}

/**
 * Checks whether the set name has already been taken in this project.
 */
watch(
  () => artifactSaveStore.editedArtifact.name,
  (newName) => {
    if (nameCheckTimer.value) {
      clearTimeout(nameCheckTimer.value);
    }

    artifactSaveStore.isNameValid = false;
    nameCheckLoading.value = true;
    nameCheckTimer.value = setTimeout(() => {
      if (!newName) {
        artifactSaveStore.isNameValid = false;
        nameCheckLoading.value = false;
      } else if (!artifactSaveStore.hasNameChanged) {
        artifactSaveStore.isNameValid = true;
        nameCheckLoading.value = false;
      } else {
        getDoesArtifactExist(projectStore.versionId, newName)
          .then((nameExists) => {
            artifactSaveStore.isNameValid = !nameExists;
            nameCheckLoading.value = false;
          })
          .catch(() => {
            artifactSaveStore.isNameValid = false;
            nameCheckLoading.value = false;
          });
      }
    }, 500);
  }
);

watch(
  () => artifactSaveStore.editedArtifact.type,
  () => artifactSaveStore.updateArtifactType()
);
</script>
