<template>
  <v-data-table
    show-select
    dense
    single-select
    v-model="selected"
    class="elevation-1"
    checkbox-color="primary"
    :headers="headers"
    :items="items"
    :items-per-page="5"
    :item-key="itemKey"
    :loading="isLoading"
    :search="search"
    :no-data-text="noDataText"
    @item-selected="$emit('onSelectItem', $event)"
  >
    <template v-slot:top>
      <slot name="deleteItemDialogue" />
      <slot name="editItemDialogue" />
      <slot name="addItemDialogue" />
      <v-row class="ma-3 pa-0">
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
            <v-btn icon @click="$emit('onRefresh')">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-row>
        </v-col>
      </v-row>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon
        v-if="hasEdit"
        small
        class="mr-2"
        @click="$emit('onEditItem', item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon v-if="hasDelete" small @click="$emit('onDeleteItem', item)">
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:footer>
      <v-row justify="end" class="mt-1">
        <v-btn fab small color="secondary" @click="$emit('onAddItem')">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-row>
    </template>
  </v-data-table>
</template>

<script lang="ts">
/* eslint-disable @typescript-eslint/no-explicit-any */
//waiting for generics to be added to vue: https://github.com/vuejs/rfcs/pull/310
import { DataItemProps, DataTableHeader } from "vuetify";
import { PropType } from "vue";
import Vue from "vue";

export default Vue.extend({
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
      required: true,
    },
    isLoading: {
      type: Boolean,
      required: true,
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
