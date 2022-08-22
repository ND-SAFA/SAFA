<template>
  <v-container
    v-if="isTableView"
    style="height: 100%"
    :class="isVisible ? 'artifact-view visible' : 'artifact-view'"
  >
    <v-data-table
      show-group-by
      show-expand
      single-expand
      fixed-header
      :headers="headers"
      :items="items"
      :search="searchText"
      :sort-by.sync="sortBy"
      :group-by.sync="groupBy"
      :group-desc.sync="groupDesc"
      :sort-desc.sync="sortDesc"
      :expanded="expanded"
      :item-class="getItemBackground"
      :items-per-page="50"
      @click:row="handleView($event)"
    >
      <template v-slot:top>
        <artifact-table-header
          :headers="headers"
          :group-by.sync="groupBy"
          :sort-by.sync="sortBy"
          :group-desc.sync="groupDesc"
          :sort-desc.sync="sortDesc"
          :search-text.sync="searchText"
          @filter="selectedDeltaTypes = $event"
        />
      </template>

      <template v-slot:[`group.header`]="data">
        <table-group-header :data="data" />
      </template>

      <template v-slot:[`item.name`]="{ item }">
        <td class="v-data-table__divider">
          <artifact-table-row-name :artifact="item" />
        </td>
      </template>

      <template v-slot:[`item.type`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip :value="item.type" artifact-type />
        </td>
      </template>

      <template
        v-for="column in columns"
        v-slot:[`item.${column.id}`]="{ item }"
      >
        <td :key="column.id" class="v-data-table__divider">
          <artifact-table-cell :column="column" :item="item" />
        </td>
      </template>

      <template v-slot:[`item.actions`]="{ item }">
        <td @click.stop="">
          <artifact-table-row-actions :artifact="item" />
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
  artifactModule,
  artifactSelectionModule,
  deltaModule,
  documentModule,
} from "@/store";
import { appStore } from "@/hooks";
import {
  Typography,
  AttributeChip,
  TableGroupHeader,
} from "@/components/common";
import ArtifactTableHeader from "./ArtifactTableHeader.vue";
import ArtifactTableCell from "./ArtifactTableCell.vue";
import ArtifactTableRowName from "./ArtifactTableRowName.vue";
import ArtifactTableRowActions from "./ArtifactTableRowActions.vue";

/**
 * Represents a table of artifacts.
 */
export default Vue.extend({
  name: "ArtifactTable",
  components: {
    ArtifactTableRowActions,
    AttributeChip,
    Typography,
    ArtifactTableHeader,
    ArtifactTableCell,
    ArtifactTableRowName,
    TableGroupHeader,
  },
  data() {
    return {
      searchText: "",
      sortBy: ["name"] as (keyof FlatArtifact)[],
      groupBy: "type" as keyof FlatArtifact,
      sortDesc: false,
      groupDesc: false,
      selectedDeltaTypes: [] as ArtifactDeltaState[],
      expanded: [] as ArtifactModel[],
    };
  },
  computed: {
    /**
     * @return Whether to render the artifact table.
     */
    isVisible(): boolean {
      return !appStore.isLoading && documentModule.isTableDocument;
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
          divider: true,
        },
        {
          text: "Type",
          value: "type",
          width: "200px",
          filterable: true,
          divider: true,
        },
        ...documentModule.tableColumns.map((col) => ({
          text: col.name,
          value: col.id,
          width: "300px",
          divider: true,
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
  },
});
</script>
