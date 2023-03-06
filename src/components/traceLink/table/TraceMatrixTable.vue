<template>
  <panel-card>
    <v-data-table
      single-select
      show-group-by
      fixed-header
      height="60vh"
      v-model="selected"
      :headers="headers"
      :items="artifactRows"
      :search="searchText"
      :loading="isLoading"
      :sort-by.sync="sortBy"
      :group-by.sync="groupBy"
      :group-desc.sync="groupDesc"
      :sort-desc.sync="sortDesc"
      item-key="name"
      :items-per-page="50"
      @click:row="handleView($event)"
      data-cy="view-trace-matrix-table"
      class="mt-4 trace-matrix-table"
    >
      <template v-slot:top>
        <trace-matrix-table-header
          :headers="headers"
          :search-text.sync="searchText"
          :group-by.sync="groupBy"
          :sort-by.sync="sortBy"
          :sort-desc.sync="sortDesc"
          :group-desc.sync="groupDesc"
          :row-types.sync="rowTypes"
          :col-types.sync="colTypes"
        />
      </template>

      <template v-slot:[`group.header`]="data">
        <table-group-header :data="data" />
      </template>

      <template v-slot:[`item.type`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip :value="item.type" artifact-type />
        </td>
      </template>

      <template
        v-for="artifact in artifactColumns"
        v-slot:[`item.${artifact.id}`]="{ item }"
      >
        <trace-matrix-chip
          :key="artifact.id"
          :source="item"
          :target="artifact"
        />
      </template>
    </v-data-table>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { DataTableHeader } from "vuetify";
import { ArtifactSchema, FlatArtifact } from "@/types";
import { appStore, artifactStore, selectionStore } from "@/hooks";
import {
  AttributeChip,
  TableGroupHeader,
  PanelCard,
} from "@/components/common";
import TraceMatrixChip from "./TraceMatrixChip.vue";
import TraceMatrixTableHeader from "./TraceMatrixTableHeader.vue";

/**
 * Displays a matrix of artifacts, showing their relationships.
 */
export default Vue.extend({
  name: "TraceMatrixTable",
  components: {
    TraceMatrixChip,
    TraceMatrixTableHeader,
    PanelCard,
    TableGroupHeader,
    AttributeChip,
  },
  data() {
    return {
      searchText: "",
      sortBy: ["name"],
      groupBy: "type",
      sortDesc: false,
      groupDesc: false,
      rowTypes: [] as string[],
      colTypes: [] as string[],
      selected: [] as FlatArtifact[],
    };
  },
  computed: {
    /**
     * @return Whether the app is loading.
     */
    isLoading() {
      return appStore.isLoading > 0;
    },
    /**
     * @return All artifacts that represent all rows.
     */
    artifactRows(): ArtifactSchema[] {
      return artifactStore.currentArtifacts.filter(
        ({ type }) => this.rowTypes.length === 0 || this.rowTypes.includes(type)
      );
    },
    /**
     * @return The artifacts that represent all columns.
     */
    artifactColumns(): ArtifactSchema[] {
      return artifactStore.currentArtifacts.filter(
        ({ type }) => this.colTypes.length === 0 || this.colTypes.includes(type)
      );
    },
    /**
     * @return All columns to render.
     */
    headers(): Partial<DataTableHeader>[] {
      return [
        {
          text: "Name",
          value: "name",
          sortable: true,
          filterable: true,
          divider: true,
          width: "200px",
        },
        {
          text: "Type",
          value: "type",
          sortable: true,
          filterable: true,
          divider: true,
          width: "200px",
        },
        ...this.artifactColumns.map(({ id, name }) => ({
          text: name,
          value: id,
          sortable: true,
          filterable: true,
          groupable: false,
          divider: true,
          width: "100px",
        })),
      ];
    },
  },
  methods: {
    /**
     * Handles viewing an artifact.
     * @param item - The artifact to view.
     */
    handleView(item: FlatArtifact) {
      if (selectionStore.selectedArtifact?.id === item.id) {
        this.selected = [];
      } else {
        this.selected = [item];
      }
    },
  },
  watch: {
    /**
     * Updates the selection store when the selected artifact changes.
     */
    selected(items: FlatArtifact[]) {
      if (items.length === 0) {
        selectionStore.clearSelections();
      } else {
        selectionStore.selectArtifact(items[0].id);
      }
    },
  },
});
</script>
