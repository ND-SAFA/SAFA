<template>
  <v-row dense class="mb-2">
    <v-col cols="12">
      <FlexBox align="center">
        <v-text-field
          v-model="searchText"
          dense
          outlined
          clearable
          hide-details
          label="Search"
          style="width: 100%"
          append-icon="mdi-magnify"
        />
        <CommitButtons v-if="showCommitButtons" color="primary" class="mx-2" />
      </FlexBox>
    </v-col>
    <v-col cols="12">
      <FlexBox>
        <v-autocomplete
          v-model="groupBy"
          clearable
          outlined
          dense
          hide-details
          label="Group By"
          :items="options"
          item-text="text"
          item-value="value"
          :prepend-inner-icon="`mdi-arrow-${
            groupDesc ? 'up' : 'down'
          }-thin-circle-outline`"
          data-cy="artifact-table-group-by"
          style="max-width: 300px"
          @click:prepend-inner="groupDesc = !groupDesc"
        />
        <v-autocomplete
          v-model="sortBy"
          outlined
          multiple
          dense
          hide-details
          label="Sort By"
          :items="options"
          item-text="text"
          item-value="value"
          class="mx-2"
          :prepend-inner-icon="`mdi-arrow-${
            sortDesc ? 'up' : 'down'
          }-thin-circle-outline`"
          data-cy="artifact-table-sort-by"
          style="max-width: 300px"
          @click:prepend-inner="sortDesc = !sortDesc"
        />
        <slot name="right" />
      </FlexBox>
    </v-col>
    <v-col cols="12">
      <slot name="bottom" />
    </v-col>
  </v-row>
</template>

<script lang="ts">
/**
 * Renders the header for a table.
 */
export default {
  name: "TableHeader",
};
</script>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch, computed } from "vue";
import { DataTableHeader } from "@/types";
import { FlexBox } from "@/components/common/layout";
import { CommitButtons } from "@/components/common/button";

const props = defineProps<{
  headers: DataTableHeader[];
  searchText: string;
  groupBy: string;
  sortBy: string[];
  groupDesc: boolean;
  sortDesc: boolean;
  showCommitButtons?: boolean;
}>();

const emit = defineEmits<{
  (e: "update:searchText", text: string): void;
  (e: "update:sortBy", values: string[]): void;
  (e: "update:sortDesc", descending: boolean): void;
  (e: "update:groupBy", value: string): void;
  (e: "update:groupDesc", descending: boolean): void;
}>();

const searchText = ref(props.searchText);
const sortBy = ref(props.sortBy);
const sortDesc = ref(props.sortDesc);
const groupBy = ref(props.groupBy);
const groupDesc = ref(props.groupDesc);

const options = computed(() =>
  props.headers
    .filter(({ text }: DataTableHeader) => !!text && text !== "Actions")
    .map(({ text, value }: DataTableHeader) => ({ text, value }))
);

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
</script>
