<template>
  <v-container
    v-if="isTableView"
    :class="isVisible ? 'artifact-view visible' : 'artifact-view'"
  >
    <v-data-table
      class="elevation-1"
      :headers="headers"
      :items="items"
      :search="searchText"
      :item-class="getItemBackground"
    >
      <template v-slot:top>
        <artifact-table-header
          @search="searchText = $event"
          @filter="selectedDeltaTypes = $event"
        />
      </template>

      <template v-slot:item.type="{ item }">
        <artifact-table-chip :text="item.type" />
      </template>

      <template
        v-for="{ id, dataType, required } in columns"
        v-slot:[`item.${id}`]="{ item }"
      >
        <v-icon v-if="required && !item[id]" :key="id" :color="errorColor">
          mdi-information-outline
        </v-icon>
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
          icon-id="mdi-view-split-vertical"
          :tooltip="`View '${item.name}'`"
          @click="handleView(item)"
        />
        <generic-icon-button
          icon-id="mdi-pencil"
          :tooltip="`Edit '${item.name}'`"
          @click="handleEdit(item)"
        />
        <generic-icon-button
          icon-id="mdi-delete"
          :tooltip="`Delete '${item.name}'`"
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
          @close="handleCloseCreate"
        />
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import {
  Artifact,
  ArtifactDeltaState,
  ColumnDataType,
  DocumentType,
  FlatArtifact,
} from "@/types";
import { ThemeColors } from "@/util";
import {
  appModule,
  artifactModule,
  artifactSelectionModule,
  deltaModule,
  documentModule,
} from "@/store";
import { handleDeleteArtifact } from "@/api";
import { GenericIconButton } from "@/components/common";
import ArtifactTableChip from "./ArtifactTableChip.vue";
import ArtifactTableHeader from "./ArtifactTableHeader.vue";
import ArtifactCreatorModal from "../ArtifactCreatorModal.vue";

/**
 * Represents a table of artifacts.
 */
export default Vue.extend({
  name: "ArtifactTable",
  components: {
    ArtifactTableHeader,
    ArtifactTableChip,
    GenericIconButton,
    ArtifactCreatorModal,
  },
  data() {
    return {
      selectedArtifact: undefined as Artifact | undefined,
      createDialogueOpen: false as boolean | DocumentType.FMEA,
      searchText: "",
      selectedDeltaTypes: [] as ArtifactDeltaState[],
      errorColor: ThemeColors.error,
    };
  },
  computed: {
    /**
     * @return Whether to render the artifact table.
     */
    isVisible(): boolean {
      return !appModule.getIsLoading && documentModule.isTableDocument;
    },
    /**
     * @return Whether delta view is enabled.
     */
    inDeltaView(): boolean {
      return deltaModule.inDeltaView;
    },
    /**
     * @return Whether table view is enabled.
     */
    isTableView(): boolean {
      return documentModule.isTableDocument;
    },

    /**
     * @return The artifact table's headers.
     */
    headers() {
      return [
        {
          text: "Name",
          value: "name",
        },
        {
          text: "Type",
          value: "type",
        },
        ...documentModule.tableColumns.map((col) => ({
          text: col.name,
          value: col.id,
        })),
        {
          text: "Actions",
          value: "actions",
          width: "150px",
        },
      ];
    },
    /**
     * @return The artifact table's columns.
     */
    columns() {
      return documentModule.tableColumns;
    },
    /**
     * @return The artifact table's items.
     */
    items(): FlatArtifact[] {
      const selectedTypes = this.inDeltaView ? [] : this.selectedDeltaTypes;
      return artifactModule.flatArtifacts.filter(
        ({ id }) =>
          selectedTypes.length === 0 ||
          selectedTypes.includes(deltaModule.getArtifactDeltaType(id))
      );
    },
    /**
     * @return The title of the artifact creator.
     */
    artifactCreatorTitle(): string {
      return this.selectedArtifact ? "Edit Artifact" : "Create Artifact";
    },
  },
  methods: {
    /**
     * Opens the view artifact side panel.
     * @param artifact - The artifact to view.
     */
    handleView(artifact: Artifact) {
      if (artifactSelectionModule.getSelectedArtifactId === artifact.id) {
        artifactSelectionModule.clearSelections();
      } else {
        artifactSelectionModule.selectArtifact(artifact.id);
      }
    },
    /**
     * Opens the edit artifact window.
     * @param artifact - The artifact to edit.
     */
    handleEdit(artifact: Artifact) {
      this.selectedArtifact = artifact;
      this.createDialogueOpen = true;
    },
    /**
     * Opens the delete artifact window.
     * @param artifact - The artifact to delete.
     */
    handleDelete(artifact: Artifact) {
      handleDeleteArtifact(artifact);
    },
    /**
     * Opens the create artifact window.
     */
    handleCreate() {
      this.createDialogueOpen = DocumentType.FMEA;
    },
    /**
     * Closes the create artifact window.
     */
    handleCloseCreate() {
      this.createDialogueOpen = false;
      this.selectedArtifact = undefined;
    },
    /**
     * @param dataType - The data type to check.
     * @return Whether the data type is free text.
     */
    isFreeText(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.FREE_TEXT;
    },
    /**
     * @param dataType - The data type to check.
     * @return Whether the data type is a relation.
     */
    isRelation(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.RELATION;
    },
    /**
     * @param dataType - The data type to check.
     * @return Whether the data type is a select.
     */
    isSelect(dataType: ColumnDataType): boolean {
      return dataType === ColumnDataType.SELECT;
    },
    /**
     * Returns the artifact name of the given artifact id.
     * @param id - The artifact to find.
     * @return The artifact name.
     */
    getArtifactName(id: string): string {
      return artifactModule.getArtifactById(id).name;
    },
    /**
     * Returns the value of an array custom field.
     * @param itemValue - The stored array value.
     * @return The stored value as an array.
     */
    getArrayValue(itemValue?: string): string[] {
      return itemValue?.split("||") || [];
    },

    /**
     * Returns the background class name of an artifact row.
     * @param item - The artifact to display.
     * @return The class name to add to the artifact.
     */
    getItemBackground(item: Artifact): string {
      if (artifactSelectionModule.getSelectedArtifactId === item.id) {
        return "artifact-selected";
      } else {
        const deltaState = deltaModule.getArtifactDeltaType(item.id);

        return `artifact-${deltaState.toLowerCase()}`;
      }
    },
  },
});
</script>
