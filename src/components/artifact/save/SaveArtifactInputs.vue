<template>
  <div>
    <text-input
      v-if="!store.isFTA"
      v-model="store.editedArtifact.name"
      label="Artifact Name"
      hint="Please select an identifier for the artifact"
      :error-message="artifactApiStore.nameError"
      :loading="artifactApiStore.nameLoading"
      class="q-mb-md"
      data-cy="input-artifact-name"
    >
      <template #append>
        <icon-button
          :loading="artifactGenerationApiStore.nameGenLoading"
          tooltip="Generate the name based on the body"
          icon="generate"
          @click="handleGenerateName"
        />
      </template>
    </text-input>
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
          :loading="artifactGenerationApiStore.bodyGenLoading"
          tooltip="Generate the body based on a prompt"
          icon="generate"
          @click="handleGenerateBody"
        />
      </template>
    </text-input>

    <text-input
      v-if="!store.isFTA && store.hasSummary"
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
import { computed } from "vue";
import { documentTypeMap, logicTypeOptions, safetyCaseOptions } from "@/util";
import {
  artifactGenerationApiStore,
  artifactSaveStore,
  documentStore,
  artifactApiStore,
} from "@/hooks";
import {
  ArtifactInput,
  ArtifactTypeInput,
  AttributeListInput,
  TextInput,
  SelectInput,
  IconButton,
} from "@/components/common";

const safetyCaseTypes = safetyCaseOptions();
const logicTypes = logicTypeOptions();

const store = computed(() => artifactSaveStore);

const documentTypes = computed(
  () => documentTypeMap()[documentStore.currentType]
);

const showDocumentType = computed(() => documentTypes.value.length > 1);

/**
 * Generates the name of the artifact based on the body.
 */
function handleGenerateName() {
  artifactGenerationApiStore.handleGenerateName();
}

/**
 * Generates the body of the artifact based on a prompt.
 */
function handleGenerateBody() {
  artifactGenerationApiStore.handleGenerateBody();
}
</script>
