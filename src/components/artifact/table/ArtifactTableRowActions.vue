<template>
  <flex-box>
    <generic-icon-button
      icon-id="mdi-pencil"
      :tooltip="`Edit '${artifact.name}'`"
      @click="handleEdit(artifact)"
      data-cy="button-artifact-edit-icon"
    />
    <generic-icon-button
      icon-id="mdi-delete"
      :tooltip="`Delete '${artifact.name}'`"
      @click="handleDelete(artifact)"
      data-cy="button-artifact-delete-icon"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactModel } from "@/types";
import { appStore, selectionStore } from "@/hooks";
import { handleDeleteArtifact } from "@/api";
import { FlexBox, GenericIconButton } from "@/components/common";

/**
 * Represents actions for an artifact.
 */
export default Vue.extend({
  name: "ArtifactTableRowActions",
  components: {
    FlexBox,
    GenericIconButton,
  },
  props: {
    artifact: Object as PropType<ArtifactModel>,
  },
  methods: {
    /**
     * Opens the edit artifact window.
     * @param artifact - The artifact to edit.
     */
    handleEdit(artifact: ArtifactModel) {
      selectionStore.selectArtifact(artifact.id);
      appStore.openArtifactCreatorTo({
        isNewArtifact: false,
      });
    },
    /**
     * Opens the delete artifact window.
     * @param artifact - The artifact to delete.
     */
    handleDelete(artifact: ArtifactModel) {
      handleDeleteArtifact(artifact, {});
    },
  },
});
</script>
