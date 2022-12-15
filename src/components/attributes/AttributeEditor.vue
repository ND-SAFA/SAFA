<template>
  <v-navigation-drawer absolute permanent width="33%">
    <flex-box
      t="6"
      full-width
      justify="space-between"
      align="center"
      class="px-4"
    >
      <typography v-if="createOpen" variant="subtitle" value="New Attribute" />
      <v-spacer />
      <v-btn v-if="!createOpen" text color="primary" @click="createOpen = true">
        <v-icon>mdi-plus</v-icon>
        Add Attribute
      </v-btn>
      <v-btn v-else text @click="createOpen = false">
        <v-icon>mdi-close</v-icon>
        Cancel
      </v-btn>
    </flex-box>
    <save-attribute v-if="createOpen" />
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
import Typography from "@/components/common/display/Typography.vue";
import SaveAttribute from "./SaveAttribute.vue";

/**
 * Renders the list of project attributes and allows for editing them.
 */
export default Vue.extend({
  name: "AttributeEditor",
  components: { Typography, FlexBox, SaveAttribute, ToggleList },
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
