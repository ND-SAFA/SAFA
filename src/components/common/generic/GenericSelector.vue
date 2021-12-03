<template>
  <v-data-table
    :show-select="hasSelect"
    dense
    single-select
    v-model="selected"
    checkbox-color="primary"
    :headers="headers"
    :items="items"
    :items-per-page="5"
    :item-key="itemKey"
    :loading="isLoading"
    :search="search"
    :no-data-text="noDataText"
    @item-selected="$emit('item:select', $event)"
  >
    <template v-slot:top>
      <slot name="deleteItemDialogue" />
      <slot name="editItemDialogue" />
      <slot name="addItemDialogue" />
      <v-row class="ma-1">
        <v-col cols="11" class="ma-0 pa-0">
          <v-text-field
            v-model="search"
            label="Search"
            rounded
            solo
            dense
            prepend-inner-icon="mdi-magnify"
          />
        </v-col>
        <v-col cols="1" class="ma-0 pa-0">
          <v-row justify="center" class="ma-0 pa-0">
            <generic-icon-button
              tooltip="Refresh"
              icon-id="mdi-refresh"
              @click="$emit('refresh')"
            />
          </v-row>
        </v-col>
      </v-row>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <generic-icon-button
        v-if="hasEdit"
        icon-id="mdi-pencil"
        tooltip="Edit"
        @click="$emit('item:edit', item)"
      />
      <generic-icon-button
        v-if="hasDelete"
        icon-id="mdi-delete"
        tooltip="Delete"
        @click="$emit('item:delete', item)"
      />
    </template>
    <template v-slot:footer>
      <v-row justify="end" class="mr-2 mt-1">
        <generic-icon-button
          fab
          color="primary"
          icon-id="mdi-plus"
          tooltip="Create"
          @click="$emit('item:add')"
        />
      </v-row>
    </template>
  </v-data-table>
</template>

<script lang="ts">
/* eslint-disable @typescript-eslint/no-explicit-any */
//waiting for generics to be added to vue: https://github.com/vuejs/rfcs/pull/310
import { DataItemProps, DataTableHeader } from "vuetify";
import Vue, { PropType } from "vue";
import GenericIconButton from "@/components/common/generic/GenericIconButton.vue";

/**
 * Displays a generic selector.
 *
 * @emits-1 `refresh` - On refresh.
 * @emits-2 `item:select` - On select item.
 * @emits-3 `item:edit` - On edit item.
 * @emits-4 `item:delete` - On delete item.
 * @emits-5 `item:add` - On add item.
 */
export default Vue.extend({
  name: "generic-selector",
  components: { GenericIconButton },
  props: {
    headers: {
      type: Array as PropType<DataTableHeader[]>,
      required: true,
    },
    items: {
      type: Array as PropType<DataItemProps[]>,
      required: true,
    },
    itemKey: {
      type: String,
      required: true,
    },
    noDataText: {
      type: String,
      required: false,
      default: "No items exists.",
    },
    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
    hasEdit: {
      type: Boolean,
      required: false,
      default: true,
    },
    hasDelete: {
      type: Boolean,
      required: false,
      default: true,
    },
    hasSelect: {
      type: Boolean,
      required: false,
      default: true,
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      search: "",
      selected: [] as DataItemProps[],
      previousItems: [] as DataItemProps[],
    };
  },
  methods: {
    clearData() {
      this.selected = [];
      this.search = "";
    },
  },
  watch: {
    items(newItems: DataItemProps[]) {
      if (this.previousItems.length === 0 && newItems.length > 0) {
        //selects any new item added
        this.previousItems = newItems;
      } else if (this.previousItems.length < newItems.length) {
        const defaultItem: DataItemProps = this.items[0];
        this.selected = [defaultItem];
        this.previousItems = newItems;
      }
    },
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.clearData();
      }
    },
  },
});
</script>
