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
    :show-expand="showExpand"
    @item-selected="$emit('item:select', $event)"
    @click:row="handleClick"
    data-cy="generic-selector-table"
  >
    <slot />
    <template v-slot:top>
      <slot name="deleteItemDialogue" />
      <slot name="editItemDialogue" />
      <slot name="addItemDialogue" />
      <flex-box v-if="!minimal" align="center" justify="space-between" y="2">
        <v-text-field
          v-model="search"
          label="Search"
          outlined
          dense
          hide-details
          class="mr-1"
          prepend-inner-icon="mdi-magnify"
          data-cy="input-selector-search"
        />
        <icon-button
          tooltip="Refresh"
          icon-id="mdi-refresh"
          data-cy="button-selector-reload"
          @click="$emit('refresh')"
        />
      </flex-box>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <td @click.stop="">
        <flex-box>
          <slot name="item.actions" :item="item" />
          <icon-button
            v-if="hasEdit"
            icon-id="mdi-pencil"
            tooltip="Edit"
            data-cy="button-selector-edit"
            @click="$emit('item:edit', item)"
          />
          <icon-button
            v-if="isDeleteEnabled(item)"
            icon-id="mdi-delete"
            tooltip="Delete"
            data-cy="button-selector-delete"
            @click="$emit('item:delete', item)"
          />
        </flex-box>
      </td>
    </template>
    <template v-slot:[`footer.prepend`]>
      <div class="py-3">
        <icon-button
          v-if="!minimal && hasAdd"
          fab
          color="primary"
          icon-id="mdi-plus"
          tooltip="Create"
          data-cy="button-selector-add"
          @click="$emit('item:add')"
        />
      </div>
    </template>
    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length" data-cy="table-generic-selector">
        <slot name="expanded-item" :item="item" />
      </td>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DataTableHeader } from "@/types";
import { FlexBox } from "@/components/common/layout";
import { IconButton } from "@/components/common/button";

/**
 * Displays a generic selector.
 *
 * @emits-1 `refresh` - On refresh.
 * @emits-2 `item:select` (item: Record<string, unknown> | undefined) - On select item.
 * @emits-3 `item:edit` (item: Record<string, unknown>) - On edit item.
 * @emits-4 `item:delete` (item: Record<string, unknown>) - On delete item.
 * @emits-5 `item:add` - On add item.
 */
export default Vue.extend({
  name: "TableSelector",
  components: { FlexBox, IconButton },
  props: {
    headers: {
      type: Array as PropType<DataTableHeader[]>,
      required: true,
    },
    items: {
      type: Array as PropType<Record<string, unknown>[]>,
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
    hasAdd: {
      type: Boolean,
      required: false,
      default: true,
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
    hasDeleteForIndexes: {
      type: Array,
      required: false,
    },
    canDeleteLastItem: {
      type: Boolean,
      required: false,
      default: true,
    },
    hasSelect: {
      type: Boolean,
      required: false,
      default: false,
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
    minimal: {
      type: Boolean,
      default: false,
    },
    showExpand: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      search: "",
      selected: [] as Record<string, unknown>[],
      previousItems: [] as Record<string, unknown>[],
    };
  },
  methods: {
    /**
     * Clears all selected data.
     */
    clearData() {
      this.selected = [];
      this.search = "";
    },
    /**
     * Returns whether delete is enabled for the given item.
     * @param item - The item to check.
     * @return Whether the item is deletable.
     */
    isDeleteEnabled(item: Record<string, unknown>): boolean {
      const index = this.items.indexOf(item);
      const isNotLastItem = index !== this.items.length - 1;

      return (
        (this.hasDelete || this.hasDeleteForIndexes?.includes(index)) &&
        (this.canDeleteLastItem || isNotLastItem)
      );
    },
    /**
     * Selects the clicked item.
     * @param item - The item to select.
     */
    handleClick(item: Record<string, unknown>): void {
      if (this.selected[0] !== item) {
        this.selected = [item];
        this.$emit("item:select", item);
      } else {
        this.selected = [];
        this.$emit("item:select");
      }
    },
  },
  watch: {
    /**
     * Resets selected when new items are loaded.
     */
    items(newItems: Record<string, unknown>[]) {
      this.selected = [];
      this.previousItems = newItems;
    },
    /**
     * Clears data when the selector opens.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.clearData();
    },
  },
});
</script>
