<template>
  <v-container>
    <v-data-table class="elevation-1" :headers="headers" :items="items">
      <template v-slot:top>
        <v-container>
          TODO: Add New Artifacts Button/Modal, Edit Document Columns
          Button/Modal, Edit/Delete Modals
        </v-container>
      </template>
      <template
        v-for="textName in textColumnNames"
        v-slot:[textName]="{ item }"
      >
        Text
      </template>
      <template
        v-for="relName in relationColumnNames"
        v-slot:[relName]="{ item }"
      >
        Relation
      </template>
      <template
        v-for="selName in selectColumnNames"
        v-slot:[selName]="{ item }"
      >
        Select
      </template>
      <template v-slot:item.actions="{ item }">
        <generic-icon-button
          icon-id="mdi-pencil"
          tooltip="Edit"
          @click="editItem(item)"
        />
        <generic-icon-button
          icon-id="mdi-delete "
          tooltip="Delete"
          @click="deleteItem(item)"
        />
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { artifactModule, documentModule } from "@/store";
import { Artifact, ColumnDataType } from "@/types";
import { GenericIconButton } from "@/components/common";

/**
 * Represents a table of artifacts.
 */
export default Vue.extend({
  name: "ArtifactTable",
  components: { GenericIconButton },
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
        },
      ];
    },
    textColumnNames() {
      return documentModule.tableColumns
        .filter(({ dataType }) => dataType === ColumnDataType.FREE_TEXT)
        .map(({ id }) => `item.${id}`);
    },
    relationColumnNames() {
      return documentModule.tableColumns
        .filter(({ dataType }) => dataType === ColumnDataType.RELATION)
        .map(({ id }) => `item.${id}`);
    },
    selectColumnNames() {
      return documentModule.tableColumns
        .filter(({ dataType }) => dataType === ColumnDataType.SELECT)
        .map(({ id }) => `item.${id}`);
    },

    items() {
      return artifactModule.artifacts;
    },
  },
  methods: {
    editItem(artifact: Artifact) {
      console.log("TODO: edit");
    },
    deleteItem(artifact: Artifact) {
      console.log("TODO: delete");
    },
  },
});
</script>

<style scoped></style>
