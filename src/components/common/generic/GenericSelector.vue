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
    @item-selected="$emit('item:select', $event, true)"
  >
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
        <generic-icon-button
          tooltip="Refresh"
          icon-id="mdi-refresh"
          data-cy="button-selector-reload"
          @click="$emit('refresh')"
        />
      </flex-box>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <flex-box>
        <generic-icon-button
          v-if="hasEdit"
          icon-id="mdi-pencil"
          tooltip="Edit"
          data-cy="button-selector-edit"
          @click="$emit('item:edit', item)"
        />
        <generic-icon-button
          v-if="isDeleteEnabled(item)"
          icon-id="mdi-delete"
          tooltip="Delete"
          data-cy="button-selector-delete"
          @click="$emit('item:delete', item)"
        />
      </flex-box>
    </template>
    <template v-slot:[`footer.prepend`]>
      <div class="py-3">
        <generic-icon-button
          v-if="!minimal"
          fab
          color="primary"
          icon-id="mdi-plus"
          tooltip="Create"
          data-cy="button-selector-add"
          @click="$emit('item:add')"
        />
      </div>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DataItemProps, DataTableHeader } from "vuetify";
import FlexBox from "@/components/common/display/FlexBox.vue";
import GenericIconButton from "./GenericIconButton.vue";

/**
 * Displays a generic selector.
 *
 * @emits-1 `refresh` - On refresh.
 * @emits-2 `item:select` (item: DataItemProps) - On select item.
 * @emits-3 `item:edit` (item: DataItemProps) - On edit item.
 * @emits-4 `item:delete` (item: DataItemProps) - On delete item.
 * @emits-5 `item:add` - On add item.
 */
export default Vue.extend({
  name: "GenericSelector",
  components: { FlexBox, GenericIconButton },
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
      default: true,
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
    minimal: {
      type: Boolean,
      default: false,
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
    isDeleteEnabled(item: DataItemProps): boolean {
      const index = this.items.indexOf(item);
      const isNotLastItem = index !== this.items.length - 1;

      return (
        (this.hasDelete || this.hasDeleteForIndexes?.includes(index)) &&
        (this.canDeleteLastItem || isNotLastItem)
      );
    },
  },
  /**
   * If no item is selected, the first item will be selected on mount.
   */
  mounted() {
    if (this.selected.length === 0 && this.items.length > 0) {
      this.selected = [this.items[0]];
      this.$emit("item:select", { item: this.items[0], value: true });
    }
  },
  watch: {
    /**
     * Select the first item when new items are loaded.
     */
    items(newItems: DataItemProps[]) {
      this.selected = [this.items[0]];
      this.previousItems = newItems;
      this.$emit("item:select", { item: this.items[0], value: true });
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
