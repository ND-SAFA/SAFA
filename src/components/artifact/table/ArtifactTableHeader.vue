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
      <flex-box v-if="deltaStore.inDeltaView">
        <v-divider vertical />
        <v-autocomplete
          v-model="selectedDeltaTypes"
          outlined
          multiple
          dense
          hide-details
          label="Delta Types"
          :items="deltaTypes"
          item-text="name"
          item-value="id"
          class="ml-2"
          style="max-width: 300px"
        />
      </flex-box>
    </template>
  </table-header>
</template>

<script lang="ts">
/**
 * Renders a header for the artifact table.
 */
export default {
  name: "ArtifactTableHeader",
};
</script>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from "vue";
import { ArtifactDeltaState, ArtifactSchema, DataTableHeader } from "@/types";
import { deltaTypeOptions } from "@/util";
import { deltaStore, useVModel } from "@/hooks";
import { TableHeader, FlexBox } from "@/components/common";

const props = defineProps<{
  headers: DataTableHeader<ArtifactSchema>[];
  searchText: string;
  groupBy: string;
  sortBy: string[];
  groupDesc: boolean;
  sortDesc: boolean;
}>();

const emit = defineEmits<{
  (e: "update:searchText", text: string): void;
  (e: "update:sortBy", values: string[]): void;
  (e: "update:sortDesc", descending: boolean): void;
  (e: "update:groupBy", value: string): void;
  (e: "update:groupDesc", descending: boolean): void;
  (e: "filter", state: ArtifactDeltaState[]): void;
}>();

const deltaTypes = deltaTypeOptions();
const searchText = useVModel(props, "searchText");
const sortBy = useVModel(props, "sortBy");
const sortDesc = useVModel(props, "sortDesc");
const groupBy = useVModel(props, "groupBy");
const groupDesc = useVModel(props, "groupDesc");
const selectedDeltaTypes = ref<ArtifactDeltaState[]>([]);

watch(
  () => selectedDeltaTypes.value,
  () => emit("filter", selectedDeltaTypes.value)
);
</script>
