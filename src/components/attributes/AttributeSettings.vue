<template>
  <panel-card>
    <v-row>
      <v-col cols="3" class="pt-6">
        <v-btn color="primary" @click="handleAddAttribute">
          <v-icon>mdi-plus</v-icon>
          Add Attribute
        </v-btn>
        <v-list expand>
          <v-list-item
            two-line
            v-for="attribute in attributes"
            :key="attribute.key"
            @click="handleClickAttribute(attribute)"
          >
            <v-list-item-content>
              <v-list-item-title>
                <typography :value="attribute.label" />
              </v-list-item-title>
              <v-list-item-subtitle>
                <typography variant="caption" :value="attribute.key" />
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-col>
      <v-col cols="9">
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
      </v-col>
    </v-row>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { AttributeLayoutSchema, AttributeSchema, SelectOption } from "@/types";
import { attributesStore } from "@/hooks";
import {
  PanelCard,
  Typography,
  AttributeGrid,
  TabList,
} from "@/components/common";

/**
 * Renders settings for customizing artifact attributes.
 */
export default Vue.extend({
  name: "AttributeSettings",
  components: { TabList, Typography, PanelCard, AttributeGrid },
  data() {
    return {
      tab: 0,
    };
  },
  computed: {
    /**
     * @return The list of custom attributes.
     */
    attributes(): AttributeSchema[] {
      return attributesStore.attributes;
    },
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
     * Adds a new attribute.
     */
    handleAddAttribute() {
      //TODO
    },
    /**
     * Selects an attribute.
     */
    handleClickAttribute(attribute: AttributeSchema) {
      //TODO
    },
    /**
     * Adds a new attribute layout.
     */
    handleAddLayout() {
      //TODO
    },
  },
});
</script>
