<template>
  <panel-card>
    <v-data-table
      show-select
      single-select
      show-group-by
      fixed-header
      height="60vh"
      v-model="selected"
      :headers="headers"
      :items="items"
      :search="searchText"
      :loading="isLoading"
      :sort-by.sync="sortBy"
      :group-by.sync="groupBy"
      :group-desc.sync="groupDesc"
      :sort-desc.sync="sortDesc"
      item-key="name"
      :items-per-page="50"
      @click:row="handleView($event)"
      data-cy="table-trace-matrix"
      class="mt-4"
    >
      <template v-slot:top>
        <table-header
          :headers="headers"
          :search-text.sync="searchText"
          :group-by.sync="groupBy"
          :sort-by.sync="sortBy"
          :sort-desc.sync="sortDesc"
          :group-desc.sync="groupDesc"
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

      <template v-for="id in artifactColumns" v-slot:[`item.${id}`]="{ item }">
        <v-chip :key="id" v-if="item[id] === 'Parent'" color="primary">
          <v-icon style="transform: rotate(-90deg)">mdi-ray-start-arrow</v-icon>
          Parent
        </v-chip>
        <v-chip :key="id" v-else-if="item[id] === 'Child'" color="secondary">
          <v-icon style="transform: rotate(90deg)">mdi-ray-start-arrow</v-icon>
          Child
        </v-chip>
      </template>
    </v-data-table>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { DataTableHeader } from "vuetify";
import { FlatArtifact } from "@/types";
import { appStore, artifactStore, selectionStore, subtreeStore } from "@/hooks";
import {
  AttributeChip,
  TableGroupHeader,
  TableHeader,
  PanelCard,
} from "@/components/common";

/**
 * Displays a matrix of artifacts, showing their relationships.
 */
export default Vue.extend({
  name: "TraceMatrixTable",
  components: {
    PanelCard,
    TableHeader,
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
     * @return All rows to render.
     */
    items(): FlatArtifact[] {
      return artifactStore.currentArtifacts.map(({ id, name, type }) => {
        return {
          id,
          name,
          type,
          ...subtreeStore
            .getParents(id)
            .map((id) => ({ [id]: "Parent" }))
            .reduce((acc, cur) => ({ ...acc, ...cur }), {}),
          ...subtreeStore
            .getChildren(id)
            .map((id) => ({ [id]: "Child" }))
            .reduce((acc, cur) => ({ ...acc, ...cur }), {}),
        };
      });
    },
    /**
     * @return The ids of artifact columns.
     */
    artifactColumns(): string[] {
      return artifactStore.currentArtifacts.map(({ id }) => id);
    },
    /**
     * @return All columns to render.
     */
    headers(): Partial<DataTableHeader>[] {
      return [
        {
          value: "data-table-select",
          groupable: false,
        },
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
        ...artifactStore.currentArtifacts.map(({ id, name }) => ({
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
      if (selectionStore.selectedArtifactId === item.id) {
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
