<template>
  <tab-list v-model="tab" :tabs="tabs">
    <template v-slot:tabs>
      <v-btn v-if="!createOpen" text color="primary" @click="handleAddLayout">
        <v-icon>mdi-plus</v-icon>
        Add Layout
      </v-btn>
    </template>
    <v-tab-item v-for="(_, idx) in tabs" :key="idx + 1">
      <save-attribute-layout
        v-if="idx === tab"
        :layout="layouts[idx]"
        @save="handleSaveLayout(idx)"
      />
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
      createOpen: false,
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
      const tabs = attributesStore.attributeLayouts.map(({ id, name }) => ({
        id,
        name,
      }));

      if (this.createOpen) {
        tabs.push({ id: "new", name: "New Layout" });
      }

      return tabs;
    },
  },
  methods: {
    /**
     * Adds a new attribute layout.
     */
    handleAddLayout(): void {
      this.createOpen = true;
      this.tab = attributesStore.attributeLayouts.length;
    },
    /**
     * Closes the layout creator on save.
     * @param idx - The index of the saved layout.
     */
    handleSaveLayout(idx: number): void {
      this.createOpen = false;
      this.tab = idx;
    },
  },
});
</script>
