<template>
  <div class="full-width">
    <flex-box full-width align="center">
      <searchbar v-model="searchText" :label="props.searchLabel" />
      <icon-button
        dense
        :icon="props.inFullscreen ? 'fullscreen-exit' : 'fullscreen'"
        :tooltip="props.inFullscreen ? 'Exit Fullscreen' : 'Enter Fullscreen'"
        class="q-ml-md"
        @click="emit('toggle-fullscreen')"
      />
    </flex-box>
    <flex-box wrap align="center" t="2">
      <select-input
        v-model="groupBy"
        outlined
        clearable
        dense
        label="Group By"
        :options="groupOptions"
        option-value="name"
        option-label="label"
        class="q-mr-sm q-mb-sm"
        option-to-value
        data-cy="artifact-table-group-by"
      />
      <select-input
        v-if="displayOptions"
        v-model="sortBy"
        outlined
        clearable
        dense
        label="Sort By"
        :options="sortOptions"
        option-value="name"
        option-label="label"
        option-to-value
        class="q-mr-sm q-mb-sm"
        data-cy="artifact-table-sort-by"
      >
        <template #prepend>
          <div @click.stop="">
            <icon-button
              small
              tooltip="Toggle sort direction"
              :icon="sortDesc ? 'arrow-down' : 'arrow-up'"
              @click="sortDesc = !sortDesc"
            />
          </div>
        </template>
      </select-input>
      <slot v-if="displayOptions" name="header-right" />
      <icon-button
        v-if="smallWindow"
        tooltip="Toggle more options"
        class="q-mb-sm"
        color="text"
        :icon="collapsed ? 'down' : 'up'"
        @click="collapsed = !collapsed"
      />
    </flex-box>
    <slot name="header-bottom" />
  </div>
</template>

<script lang="ts">
/**
 * header inputs for a table that can be grouped and expanded.
 */
export default {
  name: "GroupableTableHeader",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { GroupableTableHeaderProps } from "@/types";
import { useScreen, useVModel } from "@/hooks";
import { Searchbar, SelectInput } from "@/components/common/input";
import { IconButton } from "@/components/common/button";
import { FlexBox } from "@/components/common/display";

const props = defineProps<GroupableTableHeaderProps>();

const emit = defineEmits<{
  (e: "update:searchText", text: string | null): void;
  (e: "update:sortBy", values: string | undefined): void;
  (e: "update:sortDesc", descending: boolean): void;
  (e: "update:groupBy", value: string | undefined): void;
  (e: "toggle-fullscreen"): void;
}>();

const { smallWindow } = useScreen();

const collapsed = ref(true);

const searchText = useVModel(props, "searchText");
const sortBy = useVModel(props, "sortBy");
const sortDesc = useVModel(props, "sortDesc");
const groupBy = useVModel(props, "groupBy");

const groupOptions = computed(() =>
  props.columns
    .filter(({ name, groupable }) => name !== "actions" && groupable !== false)
    .map(({ name, label }) => ({ name, label }))
);

const sortOptions = computed(() =>
  props.columns
    .filter(({ name, sortable }) => name !== "actions" && sortable !== false)
    .map(({ name, label }) => ({ name, label }))
);

const displayOptions = computed(() => !smallWindow.value || !collapsed.value);
</script>
