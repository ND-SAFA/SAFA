<template>
  <flex-box>
    <icon-button
      icon-id="mdi-pencil"
      :tooltip="`Edit '${artifact.name}'`"
      data-cy="button-artifact-edit-icon"
      @click="handleEdit(artifact)"
    />
    <icon-button
      icon-id="mdi-delete"
      :tooltip="`Delete '${artifact.name}'`"
      data-cy="button-artifact-delete-icon"
      @click="handleDelete(artifact)"
    />
  </flex-box>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { ArtifactSchema } from "@/types";
import { appStore, selectionStore } from "@/hooks";
import { handleDeleteArtifact } from "@/api";
import { FlexBox, IconButton } from "@/components/common";

/**
 * Represents actions for an artifact.
 */
export default defineComponent({
  name: "ArtifactTableRowActions",
  components: {
    FlexBox,
    IconButton,
  },
  props: {
    artifact: Object as PropType<ArtifactSchema>,
  },
  methods: {
    /**
     * Opens the edit artifact window.
     * @param artifact - The artifact to edit.
     */
    handleEdit(artifact: ArtifactSchema) {
      selectionStore.selectArtifact(artifact.id);
      appStore.openArtifactCreatorTo({
        isNewArtifact: false,
      });
    },
    /**
     * Opens the delete artifact window.
     * @param artifact - The artifact to delete.
     */
    handleDelete(artifact: ArtifactSchema) {
      handleDeleteArtifact(artifact, {});
    },
  },
});
</script>
