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
      :sort-by.sync="sortBy"
      :group-by.sync="groupBy"
      :group-desc.sync="groupDesc"
      :sort-desc.sync="sortDesc"
      :items-per-page="50"
      data-cy="view-artifact-table"
      class="mt-4"
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
          <artifact-table-row-name
            :artifact="item"
            data-cy="table-row-artifact"
          />
        </td>
      </template>

      <template v-slot:[`item.deltaState`]="{ item }">
        <td class="v-data-table__divider">
          <artifact-table-delta-chip :artifact="item" />
        </td>
      </template>

      <template v-slot:[`item.type`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip :value="item.type" artifact-type />
        </td>
      </template>

      <template
        v-for="attribute in attributes"
        v-slot:[`item.${attribute.key}`]="{ item }"
      >
        <td :key="attribute.key" class="v-data-table__divider">
          <attribute-display :attribute="attribute" :model="item.attributes" />
        </td>
      </template>

      <template v-slot:[`item.actions`]="{ item }">
        <td @click.stop="">
          <artifact-table-row-actions :artifact="item" />
        </td>
      </template>
    </v-data-table>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { DataTableHeader } from "vuetify";
import { ArtifactDeltaState, FlatArtifact, AttributeSchema } from "@/types";
import {
  artifactStore,
  deltaStore,
  selectionStore,
  attributesStore,
} from "@/hooks";
import {
  AttributeChip,
  TableGroupHeader,
  AttributeDisplay,
  PanelCard,
} from "@/components/common";
import ArtifactTableHeader from "./ArtifactTableHeader.vue";
import ArtifactTableRowName from "./ArtifactTableRowName.vue";
import ArtifactTableRowActions from "./ArtifactTableRowActions.vue";
import ArtifactTableDeltaChip from "./ArtifactTableDeltaChip.vue";

/**
 * Represents a table of artifacts.
 */
export default Vue.extend({
  name: "ArtifactTable",
  components: {
    PanelCard,
    AttributeDisplay,
    ArtifactTableRowActions,
    AttributeChip,
    ArtifactTableHeader,
    ArtifactTableRowName,
    TableGroupHeader,
    ArtifactTableDeltaChip,
  },
  data() {
    return {
      searchText: "",
      sortBy: ["name"] as (keyof FlatArtifact)[],
      groupBy: "type" as keyof FlatArtifact,
      sortDesc: false,
      groupDesc: false,
      selectedDeltaTypes: [] as ArtifactDeltaState[],
      selected: [] as FlatArtifact[],
    };
  },
  computed: {
    /**
     * @return Whether delta view is enabled.
     */
    inDeltaView(): boolean {
      return deltaStore.inDeltaView;
    },
    /**
     * @return The artifact table's headers.
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
        ...(deltaStore.inDeltaView
          ? [
              {
                text: "Delta State",
                value: "deltaState",
                width: "200px",
                groupable: false,
              },
            ]
          : []),
        ...attributesStore.attributes.map(({ key, label }) => ({
          text: label,
          value: key,
          width: "300px",
          divider: true,
        })),
        {
          text: "Actions",
          value: "actions",
          width: "150px",
          groupable: false,
        },
      ];
    },
    /**
     * @return The artifact table's columns.
     */
    attributes(): AttributeSchema[] {
      return attributesStore.attributes;
    },
    /**
     * @return The artifact table's items.
     */
    items(): FlatArtifact[] {
      const selectedTypes = this.inDeltaView ? this.selectedDeltaTypes : [];

      return artifactStore.flatArtifacts.filter(
        ({ id }) =>
          selectedTypes.length === 0 ||
          selectedTypes.includes(deltaStore.getArtifactDeltaType(id))
      );
    },
  },
  methods: {
    /**
     * Opens the view artifact side panel.
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
