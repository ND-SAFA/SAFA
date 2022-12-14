<template>
  <v-navigation-drawer absolute permanent width="33%">
    <flex-box t="6" column full-width align="end">
      <v-btn
        v-if="!createOpen"
        text
        class="mr-4"
        color="primary"
        @click="createOpen = true"
      >
        <v-icon>mdi-plus</v-icon>
        Add Attribute
      </v-btn>
      <v-btn v-if="createOpen" class="mr-4" text @click="createOpen = false">
        <v-icon>mdi-close</v-icon>
        Cancel
      </v-btn>
      <save-attribute v-if="createOpen" />
    </flex-box>
    <v-divider v-if="createOpen" />
    <v-list expand>
      <toggle-list
        v-for="attribute in attributes"
        :key="attribute.key"
        :title="attribute.label"
      >
        <save-attribute :attribute="attribute" />
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
import SaveAttribute from "./SaveAttribute.vue";

/**
 * Renders the list of project attributes and allows for editing them.
 */
export default Vue.extend({
  name: "AttributeEditor",
  components: { FlexBox, SaveAttribute, ToggleList },
  data() {
    return {
      typeOptions: attributeTypeOptions(),
      createOpen: false,
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
  methods: {},
});
</script>
