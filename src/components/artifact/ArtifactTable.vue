<template>
  <v-container>
    <v-data-table class="elevation-1" :headers="headers" :items="items">
      <template v-slot:top>
        <v-container> TODO: Edit Document Columns Button/Modal </v-container>
      </template>
      <template
        v-for="textName in textColumnNames"
        v-slot:[textName]="{ item }"
      >
        Text
      </template>
      <template
        v-for="relName in relationColumnNames"
        v-slot:[relName]="{ item }"
      >
        Relation
      </template>
      <template
        v-for="selName in selectColumnNames"
        v-slot:[selName]="{ item }"
      >
        Select
      </template>
      <template v-slot:item.actions="{ item }">
        <generic-icon-button
          icon-id="mdi-pencil"
          tooltip="Edit"
          @click="handleEdit(item)"
        />
        <generic-icon-button
          icon-id="mdi-delete "
          tooltip="Delete"
          @click="handleDelete(item)"
        />
      </template>
      <template v-slot:footer>
        <v-row justify="end" class="mr-2 mt-1">
          <generic-icon-button
            fab
            color="primary"
            icon-id="mdi-plus"
            tooltip="Create"
            @click="handleCreate"
          />
        </v-row>

        <artifact-creator-modal
          :title="artifactCreatorTitle"
          :is-open="createDialogueOpen"
          :artifact="selectedArtifact"
          @close="handleCloseModal"
        />
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { Artifact, ColumnDataType } from "@/types";
import { artifactModule, documentModule } from "@/store";
import { deleteArtifactFromCurrentVersion } from "@/api";
import { GenericIconButton, ArtifactCreatorModal } from "@/components/common";

/**
 * Represents a table of artifacts.
 */
export default Vue.extend({
  name: "ArtifactTable",
  components: { GenericIconButton, ArtifactCreatorModal },
  data() {
    return {
      selectedArtifact: undefined as Artifact | undefined,
      createDialogueOpen: false,
    };
  },
  computed: {
    headers() {
      return [
        {
          text: "Name",
          value: "name",
        },
        ...documentModule.tableColumns.map((col) => ({
          text: col.name,
          value: col.id,
        })),
        {
          text: "Actions",
          value: "actions",
        },
      ];
    },
    textColumnNames() {
      return documentModule.tableColumns
        .filter(({ dataType }) => dataType === ColumnDataType.FREE_TEXT)
        .map(({ id }) => `item.${id}`);
    },
    relationColumnNames() {
      return documentModule.tableColumns
        .filter(({ dataType }) => dataType === ColumnDataType.RELATION)
        .map(({ id }) => `item.${id}`);
    },
    selectColumnNames() {
      return documentModule.tableColumns
        .filter(({ dataType }) => dataType === ColumnDataType.SELECT)
        .map(({ id }) => `item.${id}`);
    },

    items() {
      return artifactModule.artifacts;
    },

    artifactCreatorTitle(): string {
      return this.selectedArtifact ? "Edit Artifact" : "Create Artifact";
    },
  },
  methods: {
    handleEdit(artifact: Artifact) {
      console.log(artifact);
      this.selectedArtifact = artifact;
      this.createDialogueOpen = true;
    },
    handleDelete(artifact: Artifact) {
      deleteArtifactFromCurrentVersion(artifact);
    },
    handleCreate() {
      this.createDialogueOpen = true;
    },
    handleCloseModal() {
      this.createDialogueOpen = false;
      this.selectedArtifact = undefined;
    },
  },
});
</script>

<style scoped></style>
