<template>
  <v-container>
    <v-data-table class="elevation-1" :headers="headers" :items="items">
      <template v-slot:top>
        <v-container class="flex">
          <table-column-editor class="ml-auto"
        /></v-container>
      </template>
      <template
        v-for="{ id, dataType, required } in columns"
        v-slot:[`item.${id}`]="{ item }"
      >
        <v-divider
          v-if="required && !item[id]"
          :key="id"
          :style="`border-color: ${errorColor}; width: 40px`"
        />
        <span v-if="isFreeText(dataType)" class="text-body-1" :key="id">
          {{ item[id] || "" }}
        </span>
        <div v-if="isRelation(dataType)" :key="id">
          <artifact-table-chip
            v-for="artifactId in getArrayValue(item[id])"
            :key="artifactId"
            :text="getArtifactName(artifactId)"
          />
        </div>
        <div v-if="isSelect(dataType)" :key="id">
          <artifact-table-chip
            v-for="val in getArrayValue(item[id])"
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
          icon-id="mdi-delete"
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
import ArtifactTableChip from "@/components/artifact/table/ArtifactTableChip.vue";
import TableColumnEditor from "@/components/artifact/table/TableColumnEditor.vue";
import { ThemeColors } from "@/util";

/**
 * Represents a table of artifacts.
 */
export default Vue.extend({
  name: "ArtifactTable",
  components: {
    TableColumnEditor,
    ArtifactTableChip,
    GenericIconButton,
    ArtifactCreatorModal,
  },
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
          width: "120px",
        },
      ];
    },
    columns() {
      return documentModule.tableColumns;
    },
    items() {
      return artifactModule.artifacts.map((artifact) => ({
        ...artifact,
        ...artifact.customFields,
      }));
    },
    artifactCreatorTitle(): string {
      return this.selectedArtifact ? "Edit Artifact" : "Create Artifact";
    },
    errorColor(): string {
      return ThemeColors.error;
    },
  },
  methods: {
    handleEdit(artifact: Artifact) {
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
    getArrayValue(itemValue?: string): string[] {
      return itemValue?.split("||") || [];
    },
  },
});
</script>

<style scoped></style>
