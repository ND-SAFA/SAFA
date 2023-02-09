<template>
  <TableHeader
    v-model:search-text="searchText"
    v-model:group-by="groupBy"
    v-model:sort-by="sortBy"
    v-model:sort-desc="sortDesc"
    v-model:group-desc="groupDesc"
    :headers="headers"
    data-cy="table-header"
  >
    <template #right>
      <FlexBox>
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
      </FlexBox>
    </template>
  </TableHeader>
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
import { defineProps, defineEmits, ref, watch } from "vue";
import { ArtifactSchema, DataTableHeader } from "@/types";
import { typeOptionsStore } from "@/hooks";
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

const searchText = ref(props.searchText);
const sortBy = ref(props.sortBy);
const sortDesc = ref(props.sortDesc);
const groupBy = ref(props.groupBy);
const groupDesc = ref(props.groupDesc);
const colTypes = ref(props.colTypes);
const rowTypes = ref(props.rowTypes);

watch(
  () => searchText.value,
  () => emit("update:searchText", searchText.value)
);

watch(
  () => sortBy.value,
  () => emit("update:sortBy", sortBy.value)
);

watch(
  () => sortDesc.value,
  () => emit("update:sortDesc", sortDesc.value)
);

watch(
  () => groupBy.value,
  () => emit("update:groupBy", groupBy.value)
);

watch(
  () => groupDesc.value,
  () => emit("update:groupDesc", groupDesc.value)
);

watch(
  () => colTypes.value,
  () => emit("update:colTypes", colTypes.value)
);

watch(
  () => rowTypes.value,
  () => emit("update:rowTypes", rowTypes.value)
);
</script>
