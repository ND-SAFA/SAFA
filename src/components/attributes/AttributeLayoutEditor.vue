<template>
  <tab-list v-model="tab" :tabs="tabs">
    <template v-slot:tabs>
      <v-btn text color="primary" @click="handleAddLayout">
        <v-icon>mdi-plus</v-icon>
        Add Layout
      </v-btn>
    </template>
    <v-tab-item v-for="(tab, idx) in tabs" :key="idx + 1">
      <save-attribute-layout :layout="layouts[idx]" />
    </v-tab-item>
  </tab-list>
</template>

<script lang="ts">
import Vue from "vue";
import { AttributeLayoutSchema, SelectOption } from "@/types";
import { attributesStore } from "@/hooks";
import { TabList } from "@/components/common";
import SaveAttributeLayout from "./SaveAttributeLayout.vue";

/**
 * Allows for editing attribute layouts.
 */
export default Vue.extend({
  name: "AttributeLayoutEditor",
  components: {
    SaveAttributeLayout,
    TabList,
  },
  data() {
    return {
      tab: 0,
    };
  },
  computed: {
    /**
     * @return The list of custom attribute layouts.
     */
    layouts(): AttributeLayoutSchema[] {
      return attributesStore.attributeLayouts;
    },
    /**
     * @return The tabs for each layout.
     */
    tabs(): SelectOption[] {
      return attributesStore.attributeLayouts.map(({ id, name }) => ({
        id,
        name,
      }));
    },
  },
  methods: {
    /**
     * Adds a new attribute layout.
     */
    handleAddLayout() {
      //TODO
    },
  },
});
</script>
