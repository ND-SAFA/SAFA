<template>
  <v-navigation-drawer absolute permanent width="33%">
    <v-btn class="ml-4 mt-6" color="primary" @click="handleAdd">
      <v-icon>mdi-plus</v-icon>
      Add Attribute
    </v-btn>
    <v-list expand>
      <toggle-list
        v-for="attribute in attributes"
        :key="attribute.key"
        :title="attribute.label"
      >
        <v-container>
          <v-text-field filled disabled label="Key" v-model="attribute.key" />
          <v-text-field filled label="Label" v-model="attribute.label" />
          <v-select
            filled
            disabled
            label="Type"
            v-model="attribute.type"
            item-text="name"
            item-value="id"
            :items="typeOptions"
          />
          <v-combobox
            v-if="attribute.type.includes('select')"
            filled
            chips
            deletable-chips
            multiple
            label="Options"
            v-model="attribute.options"
          />
          <flex-box justify="space-between">
            <v-btn text color="error" @click="handleDelete(attribute)">
              Delete
            </v-btn>
            <v-btn color="primary" @click="handleSave(attribute)">Save</v-btn>
          </flex-box>
        </v-container>
      </toggle-list>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from "vue";
import { AttributeSchema } from "@/types";
import { attributeTypeOptions } from "@/util";
import { attributesStore } from "@/hooks";
import { ToggleList, FlexBox } from "@/components/common";

/**
 * Renders the list of project attributes and allows for editing them.
 */
export default Vue.extend({
  name: "AttributeEditor",
  components: { FlexBox, ToggleList },
  data() {
    return {
      typeOptions: attributeTypeOptions(),
    };
  },
  computed: {
    /**
     * @return The list of custom attributes.
     */
    attributes(): AttributeSchema[] {
      return attributesStore.attributes;
    },
  },
  methods: {
    /**
     * Adds a new attribute.
     */
    handleAdd() {
      //TODO
    },
    /**
     * Updates an attribute.
     */
    handleSave(attribute: AttributeSchema) {
      //TODO
    },
    /**
     * Deletes an attribute.
     */
    handleDelete(attribute: AttributeSchema) {
      //TODO
    },
  },
});
</script>
