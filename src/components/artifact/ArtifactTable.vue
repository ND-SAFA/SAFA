<template>
  <v-container>
    <v-data-table class="elevation-1" :headers="headers" :items="items">
      <template v-slot:top>
        <v-container> </v-container>
      </template>
      <template
        v-for="{ id, dataType } in columns"
        v-slot:[`item.${id}`]="{ item }"
      >
        <span v-if="isFreeText(dataType)" class="text-body-1" :key="id">
          {{ item[id] }}
        </span>
        <div v-if="isRelation(dataType)" :key="id">
          <artifact-table-chip
            v-for="artifactId in item[id].split('||')"
            :key="artifactId"
            :text="getArtifactName(artifactId)"
          />
        </div>
        <div v-if="isSelect(dataType)" :key="id">
          <artifact-table-chip
            v-for="val in item[id].split('||')"
            :key="val"
            :text="val"
          />
        </div>
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
import { ArtifactCreatorModal, GenericIconButton } from "@/components/common";
import ArtifactTableChip from "@/components/artifact/ArtifactTableChip.vue";

/**
 * Represents a table of artifacts.
 */
export default Vue.extend({
  name: "ArtifactTable",
  components: { ArtifactTableChip, GenericIconButton, ArtifactCreatorModal },
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
    columns() {
      return documentModule.tableColumns;
    },
    items() {
      return artifactModule.artifacts.map((artifact) => ({
        ...artifact,
        //TODO: remove test data
        1: "A",
        2: "3681f538-0f3f-4e6e-a73c-1ecbb5033a94||bce84af9-704b-4cef-8aea-7e479e27c51f",
        3: "D||E",
      }));
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

    isFreeText(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.FREE_TEXT;
    },
    isRelation(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.RELATION;
    },
    isSelect(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.SELECT;
    },
    getArtifactName(id: string): string {
      return artifactModule.getArtifactById(id).name;
    },
  },
});
</script>

<style scoped></style>
