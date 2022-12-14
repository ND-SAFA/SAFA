<template>
  <tab-list v-model="tab" :tabs="tabs" background="inner">
    <template v-slot:tabs>
      <v-btn text color="primary" @click="handleAddLayout">
        <v-icon>mdi-plus</v-icon>
        Add Layout
      </v-btn>
    </template>
    <v-tab-item v-for="(tab, idx) in tabs" :key="idx + 1">
      <attribute-grid editable>
        <template v-slot:item="{ attribute }">
          <v-card outlined class="pa-2 mx-2">
            {{ attribute.label }}
          </v-card>
        </template>
      </attribute-grid>
    </v-tab-item>
  </tab-list>
</template>

<script lang="ts">
import Vue from "vue";
import { AttributeLayoutSchema, SelectOption } from "@/types";
import { attributesStore } from "@/hooks";
import { AttributeGrid, TabList } from "@/components/common";

/**
 * Allows for editing attribute layouts.
 */
export default Vue.extend({
  name: "AttributeLayoutEditor",
  components: { TabList, AttributeGrid },
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
