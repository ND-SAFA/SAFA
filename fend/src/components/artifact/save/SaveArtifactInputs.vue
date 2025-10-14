<template>
  <div>
    <text-input
      v-model="artifactSaveStore.editedArtifact.name"
      label="Artifact Name"
      hint="Enter a unique name for the artifact"
      :error-message="artifactApiStore.nameError"
      :loading="artifactApiStore.nameLoading"
      class="q-mb-md"
      data-cy="input-artifact-name"
    >
      <template #append>
        <icon-button
          v-if="ENABLED_FEATURES.ARTIFACT_PROMPTS"
          :loading="artifactGenerationApiStore.nameGenLoading"
          tooltip="Generate the name based on the body"
          icon="generate"
          @click="handleGenerateName"
        />
      </template>
    </text-input>

    <artifact-type-input
      v-model="artifactSaveStore.editedArtifact.type"
      label="Artifact Type"
      hint="Press enter to save a new artifact type"
      class="q-mb-md"
      data-cy="input-artifact-type"
    />

    <text-input
      v-model="artifactSaveStore.editedArtifact.body"
      label="Artifact Body"
      type="textarea"
      hint="Required"
      class="q-mb-md"
      data-cy="input-artifact-body"
    >
      <template #append>
        <icon-button
          v-if="ENABLED_FEATURES.ARTIFACT_PROMPTS"
          :loading="artifactGenerationApiStore.bodyGenLoading"
          tooltip="Generate the body based on a prompt"
          icon="generate"
          @click="handleGenerateBody"
        />
      </template>
    </text-input>

    <text-input
      v-if="artifactSaveStore.hasSummary"
      v-model="artifactSaveStore.editedArtifact.summary"
      label="Artifact Summary"
      type="textarea"
      class="q-mb-md"
      data-cy="input-artifact-summary"
    />

    <artifact-input
      v-if="!artifactSaveStore.isUpdate"
      v-model="artifactSaveStore.parentIds"
      multiple
      only-document-artifacts
      label="Parent Artifacts"
      data-cy="input-artifact-parent"
      class="q-mb-md"
    />
    <artifact-input
      v-if="!artifactSaveStore.isUpdate"
      v-model="artifactSaveStore.childIds"
      multiple
      only-document-artifacts
      label="Child Artifacts"
      data-cy="input-artifact-child"
      class="q-mb-md"
    />

    <attribute-list-input :artifact="artifactSaveStore.editedArtifact" />
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
import { ENABLED_FEATURES } from "@/util";
import {
  artifactGenerationApiStore,
  artifactSaveStore,
  artifactApiStore,
} from "@/hooks";
import {
  ArtifactInput,
  ArtifactTypeInput,
  AttributeListInput,
  TextInput,
  IconButton,
} from "@/components/common";

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
