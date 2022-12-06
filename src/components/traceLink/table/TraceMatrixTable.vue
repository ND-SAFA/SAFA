<template>
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
  </v-data-table>
</template>

<script lang="ts">
import Vue from "vue";
import { DataTableHeader } from "vuetify";
import { ArtifactSchema } from "@/types";
import { appStore, artifactStore, selectionStore, subtreeStore } from "@/hooks";
import {
  AttributeChip,
  TableGroupHeader,
  TableHeader,
} from "@/components/common";

/**
 * Displays a matrix of artifacts, showing their relationships.
 */
export default Vue.extend({
  name: "TraceMatrixTable",
  components: {
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
    items(): (Pick<ArtifactSchema, "id" | "name" | "type"> &
      Record<string, string>)[] {
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
     * @param artifact - The artifact to view.
     */
    handleView(artifact: Pick<ArtifactSchema, "id" | "name" | "type">) {
      selectionStore.toggleSelectArtifact(artifact.id);
    },
  },
});
</script>
