<template>
  <v-row dense class="mb-2">
    <v-col cols="12">
      <flex-box align="center">
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
        <commit-buttons v-if="showCommitButtons" color="primary" class="mx-2" />
      </flex-box>
    </v-col>
    <v-col cols="12">
      <flex-box>
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
      </flex-box>
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
import { defineProps, defineEmits, computed } from "vue";
import { DataTableHeader } from "@/types";
import { useVModel } from "@/hooks";
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

const searchText = useVModel(props, "searchText");
const sortBy = useVModel(props, "sortBy");
const sortDesc = useVModel(props, "sortDesc");
const groupBy = useVModel(props, "groupBy");
const groupDesc = useVModel(props, "groupDesc");

const options = computed(() =>
  props.headers
    .filter(({ text }: DataTableHeader) => !!text && text !== "Actions")
    .map(({ text, value }: DataTableHeader) => ({ text, value }))
);
</script>
