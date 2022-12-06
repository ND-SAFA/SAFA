<template>
  <v-container
    v-if="isTableView"
    style="height: 100%"
    :class="isVisible ? 'artifact-view visible' : 'artifact-view'"
  >
    <v-data-table
      show-group-by
      multi-sort
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
    >
      <template v-slot:top> </template>

      <template v-slot:[`group.header`]="data">
        <table-group-header
          show-expand
          :data="data"
          @open:all="handleOpenAll"
          @close:all="handleCloseAll"
        />
      </template>

      <template v-slot:[`item.type`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip :value="item.sourceType" artifact-type />
        </td>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { DataTableHeader } from "vuetify";
import { ArtifactSchema, TraceTableGroup } from "@/types";
import {
  appStore,
  artifactStore,
  documentStore,
  selectionStore,
} from "@/hooks";
import { AttributeChip, TableGroupHeader } from "@/components/common";

/**
 * Displays a matrix of artifacts, showing their relationships.
 */
export default Vue.extend({
  name: "TraceMatrixTable",
  components: {
    TableGroupHeader,
    AttributeChip,
  },
  data() {
    return {
      searchText: "",
      sortBy: ["type", "name"],
      groupBy: "type",
      sortDesc: false,
      groupDesc: false,
    };
  },
  computed: {
    /**
     * @return Whether table view is enabled.
     */
    isTableView(): boolean {
      return documentStore.isTableDocument;
    },
    /**
     * @return Whether the app is loading.
     */
    isLoading() {
      return appStore.isLoading > 0;
    },
    /**
     * @return Whether to render the artifact table.
     */
    isVisible(): boolean {
      return documentStore.isTableDocument;
    },
    /**
     * @return All rows to render.
     */
    items(): (Pick<ArtifactSchema, "id" | "name" | "type"> &
      Record<string, string>)[] {
      return artifactStore.currentArtifacts.map(({ id, name, type }) => ({
        id,
        name,
        type,
      }));
    },
    /**
     * @return All columns to render.
     */
    headers(): DataTableHeader[] {
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
        ...artifactStore.currentArtifacts.map(({ name }) => ({
          text: name,
          value: `artifact:${name}`,
          sortable: true,
          filterable: true,
          groupable: false,
          divider: true,
          width: "200px",
        })),
      ];
    },
  },
  methods: {
    /**
     * TODO
     * Opens all panels in the group.
     * @param data - The current grouping information.
     */
    handleOpenAll(data: TraceTableGroup) {
      console.log(data);
    },
    /**
     * TODO
     * Closes all panels in the group.
     * @param data - The current grouping information.
     */
    handleCloseAll(data: TraceTableGroup) {
      console.log(data);
    },
    /**
     * Handles viewing an artifact.
     * @param artifact - The artifact to view.
     */
    handleView(artifact: Pick<ArtifactSchema, "id" | "name" | "type">) {
      selectionStore.selectArtifact(artifact.id);
    },
  },
});
</script>
