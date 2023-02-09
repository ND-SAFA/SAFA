<template>
  <table-header
    v-model:search-text="searchText"
    v-model:group-by="groupBy"
    v-model:sort-by="sortBy"
    v-model:sort-desc="sortDesc"
    v-model:group-desc="groupDesc"
    :headers="headers"
    data-cy="table-header"
  >
    <template #right>
      <flex-box>
        <v-divider vertical />
        <v-autocomplete
          v-model="rowTypes"
          outlined
          multiple
          dense
          hide-details
          label="Row Types"
          :items="typeOptionsStore.artifactTypes"
          style="max-width: 300px"
          class="mx-2"
          data-cy="input-trace-matrix-table-row-types"
        />
        <v-autocomplete
          v-model="colTypes"
          outlined
          multiple
          dense
          hide-details
          label="Column Types"
          :items="typeOptionsStore.artifactTypes"
          style="max-width: 300px"
          data-cy="input-trace-matrix-table-col-types"
        />
      </flex-box>
    </template>
  </table-header>
</template>

<script lang="ts">
/**
 * Represents the header and inputs for a table of trace links.
 */
export default {
  name: "TraceMatrixTableHeader",
};
</script>

<script setup lang="ts">
import { defineProps, defineEmits } from "vue";
import { ArtifactSchema, DataTableHeader } from "@/types";
import { typeOptionsStore, useVModel } from "@/hooks";
import { TableHeader, FlexBox } from "@/components/common";

const props = defineProps<{
  headers: DataTableHeader<ArtifactSchema>[];
  searchText: string;
  groupBy: string;
  sortBy: string[];
  groupDesc: boolean;
  sortDesc: boolean;
  colTypes: string[];
  rowTypes: string[];
}>();

const emit = defineEmits<{
  (e: "update:searchText", text: string): void;
  (e: "update:sortBy", values: string[]): void;
  (e: "update:sortDesc", descending: boolean): void;
  (e: "update:groupBy", value: string): void;
  (e: "update:groupDesc", descending: boolean): void;
  (e: "update:colTypes", types: string[]): void;
  (e: "update:rowTypes", types: string[]): void;
}>();

const searchText = useVModel(props, "searchText");
const sortBy = useVModel(props, "sortBy");
const sortDesc = useVModel(props, "sortDesc");
const groupBy = useVModel(props, "groupBy");
const groupDesc = useVModel(props, "groupDesc");
const rowTypes = useVModel(props, "rowTypes");
const colTypes = useVModel(props, "colTypes");
</script>
