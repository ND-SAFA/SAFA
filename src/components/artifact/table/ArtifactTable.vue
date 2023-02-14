<template>
  <panel-card>
    <v-data-table
      v-model="selected"
      v-model:sort-by="sortBy"
      v-model:group-by="groupBy"
      v-model:group-desc="groupDesc"
      v-model:sort-desc="sortDesc"
      single-select
      show-group-by
      fixed-header
      height="60vh"
      :headers="headers"
      :items="items"
      :search="searchText"
      :items-per-page="50"
      data-cy="view-artifact-table"
      class="mt-4 artifact-table"
      @click:row="handleView($event)"
    >
      <template #top>
        <artifact-table-header
          v-model:group-by="groupBy"
          v-model:sort-by="sortBy"
          v-model:group-desc="groupDesc"
          v-model:sort-desc="sortDesc"
          v-model:search-text="searchText"
          :headers="headers"
          @filter="selectedDeltaTypes = $event"
        />
      </template>

      <template #[`group.header`]="data">
        <table-group-header :data="data" />
      </template>

      <template #[`item.name`]="{ item }">
        <td class="v-data-table__divider">
          <artifact-table-row-name :artifact="item" />
        </td>
      </template>

      <template #[`item.deltaState`]="{ item }">
        <td class="v-data-table__divider">
          <artifact-table-delta-chip :artifact="item" />
        </td>
      </template>

      <template #[`item.type`]="{ item }">
        <td class="v-data-table__divider">
          <attribute-chip :value="item.type" artifact-type />
        </td>
      </template>

      <template
        v-for="attribute in attributes"
        #[`item.${attribute.key}`]="{ item }"
        :key="attribute.key"
      >
        <td class="v-data-table__divider">
          <attribute-display
            hide-title
            :attribute="attribute"
            :model="item.attributes || {}"
          />
        </td>
      </template>

      <template #[`item.actions`]="{ item }">
        <td @click.stop="">
          <artifact-table-row-actions :artifact="item" />
        </td>
      </template>
    </v-data-table>
  </panel-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import {
  ArtifactDeltaState,
  FlatArtifact,
  AttributeSchema,
  DataTableHeader,
  ArtifactSchema,
} from "@/types";
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
export default defineComponent({
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
      sortBy: ["name"],
      groupBy: "type",
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
    headers(): DataTableHeader<ArtifactSchema>[] {
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
  methods: {
    /**
     * Opens the view artifact side panel.
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
});
</script>
