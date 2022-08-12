<template>
  <v-container
    v-if="isTableView"
    style="height: 100%"
    :class="isVisible ? 'artifact-view visible' : 'artifact-view'"
  >
    <v-data-table
      :headers="headers"
      :items="items"
      :search="searchText"
      :expanded="expanded"
      :item-class="getItemBackground"
      sort-by="name"
      show-group-by
      show-expand
      single-expand
      fixed-header
      :items-per-page="50"
      @click:row="handleView($event)"
    >
      <template v-slot:top>
        <artifact-table-header
          @search="searchText = $event"
          @filter="selectedDeltaTypes = $event"
        />
      </template>

      <template v-slot:[`item.name`]="{ item }">
        <td>
          <flex-box align="center">
            <artifact-table-delta-chip :artifact="item" />
            <v-icon v-if="getHasWarnings(item)" color="secondary">
              mdi-hazard-lights
            </v-icon>
            <typography l="1" :value="item.name" />
          </flex-box>
        </td>
      </template>

      <template v-slot:[`item.type`]="{ item }">
        <td>
          <artifact-table-chip :text="item.type" display-icon />
        </td>
      </template>

      <template
        v-for="column in columns"
        v-slot:[`item.${column.id}`]="{ item }"
      >
        <td :key="column.id">
          <artifact-table-cell :column="column" :item="item" />
        </td>
      </template>

      <template v-slot:[`item.actions`]="{ item }">
        <td>
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
        </td>
      </template>

      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <typography el="p" y="2" :value="item.body" />
        </td>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactModel, ArtifactDeltaState, FlatArtifact } from "@/types";
import {
  appModule,
  artifactModule,
  artifactSelectionModule,
  deltaModule,
  documentModule,
  errorModule,
} from "@/store";
import { handleDeleteArtifact } from "@/api";
import { GenericIconButton, Typography, FlexBox } from "@/components/common";
import ArtifactTableChip from "./ArtifactTableChip.vue";
import ArtifactTableHeader from "./ArtifactTableHeader.vue";
import ArtifactTableCell from "./ArtifactTableCell.vue";
import ArtifactTableDeltaChip from "./ArtifactTableDeltaChip.vue";

/**
 * Represents a table of artifacts.
 */
export default Vue.extend({
  name: "ArtifactTable",
  components: {
    FlexBox,
    Typography,
    ArtifactTableDeltaChip,
    ArtifactTableHeader,
    ArtifactTableChip,
    GenericIconButton,
    ArtifactTableCell,
  },
  data() {
    return {
      searchText: "",
      selectedDeltaTypes: [] as ArtifactDeltaState[],
      expanded: [] as ArtifactModel[],
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
          width: "200px",
          filterable: true,
        },
        {
          text: "Type",
          value: "type",
          width: "200px",
          filterable: true,
        },
        ...documentModule.tableColumns.map((col) => ({
          text: col.name,
          value: col.id,
          width: "300px",
        })),
        {
          text: "Actions",
          value: "actions",
          width: "150px",
          groupable: false,
        },
        {
          value: "data-table-expand",
          groupable: false,
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
      const selectedTypes = this.inDeltaView ? this.selectedDeltaTypes : [];

      return artifactModule.flatArtifacts.filter(
        ({ id }) =>
          selectedTypes.length === 0 ||
          selectedTypes.includes(deltaModule.getArtifactDeltaType(id))
      );
    },
  },
  methods: {
    /**
     * Opens the view artifact side panel.
     * @param artifact - The artifact to view.
     */
    handleView(artifact: ArtifactModel) {
      if (artifactSelectionModule.getSelectedArtifactId === artifact.id) {
        artifactSelectionModule.clearSelections();
        this.expanded = [];
      } else {
        artifactSelectionModule.selectArtifact(artifact.id);
        this.expanded = [artifact];
      }
    },
    /**
     * Opens the edit artifact window.
     * @param artifact - The artifact to edit.
     */
    handleEdit(artifact: ArtifactModel) {
      artifactSelectionModule.selectArtifact(artifact.id);
      appModule.openArtifactCreatorTo({
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
    /**
     * Returns the background class name of an artifact row.
     * @param item - The artifact to display.
     * @return The class name to add to the artifact.
     */
    getItemBackground(item: ArtifactModel): string {
      if (artifactSelectionModule.getSelectedArtifactId === item.id) {
        return "artifact-row-selected";
      }

      return "";
    },
    /**
     * Returns whether the artifact has any warnings.
     * @param item - The artifact to search for
     * @return Whether the artifact has warnings.
     */
    getHasWarnings(item: ArtifactModel): boolean {
      return errorModule.getWarningsByIds([item.id]).length > 0;
    },
  },
});
</script>

<style lang="scss">
.v-data-table__expanded__content {
  box-shadow: inset 0px 2px 8px -5px rgba(50, 50, 50, 0.75),
    inset 0px -2px 8px -5px rgba(50, 50, 50, 0.75) !important;
}

.artifact-view {
  tr {
    cursor: pointer;
  }
}
</style>
