<template>
  <div>
    <flex-box
      t="6"
      full-width
      wrap
      justify="space-between"
      align="center"
      class="px-4"
    >
      <typography
        variant="subtitle"
        :value="createOpen ? 'New Attribute' : 'Attributes'"
      />
      <v-spacer />
      <text-button
        v-if="!createOpen"
        text
        variant="add"
        @click="createOpen = true"
        data-cy="button-add-attribute"
      >
        Add Attribute
      </text-button>
      <text-button v-else text variant="cancel" @click="createOpen = false">
        Cancel
      </text-button>
    </flex-box>
    <save-attribute v-if="createOpen" @save="createOpen = false" />
    <v-divider v-if="createOpen" />
    <v-list expand>
      <toggle-list
        v-for="attribute in attributes"
        :key="attribute.key"
        :title="attribute.label"
      >
        <template v-slot:activator>
          <span @click.stop="">
            <icon-button
              class="ml-auto"
              icon-id="mdi-plus"
              tooltip="Add to layout"
              :is-disabled="isAttributeInLayout(attribute)"
              @click="handleAddToLayout(attribute)"
            />
          </span>
        </template>
        <save-attribute :attribute="attribute" />
      </toggle-list>
    </v-list>
    <flex-box v-if="attributes.length === 0" justify="center">
      <typography
        variant="caption"
        value="You have not yet created any custom attributes."
      />
    </flex-box>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { AttributePositionSchema, AttributeSchema } from "@/types";
import { attributeTypeOptions } from "@/util";
import { attributeLayoutSaveStore, attributesStore } from "@/hooks";
import {
  FlexBox,
  TextButton,
  ToggleList,
  Typography,
  IconButton,
} from "@/components/common";
import SaveAttribute from "./SaveAttribute.vue";

/**
 * Renders the list of project attributes and allows for editing them.
 */
export default Vue.extend({
  name: "AttributeEditor",
  components: {
    IconButton,
    TextButton,
    Typography,
    FlexBox,
    SaveAttribute,
    ToggleList,
  },
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
    /**
     * @return The store for the current layout being edited.
     */
    layoutStore() {
      return attributeLayoutSaveStore(attributesStore.selectedLayoutId);
    },
  },
  methods: {
    /**
     * @return Whether this attribute is in the current layout.
     */
    isAttributeInLayout(attribute: AttributeSchema): boolean {
      return !!this.layoutStore.editedLayout.positions.find(
        ({ key }: AttributePositionSchema) => key === attribute.key
      );
    },
    /**
     * Adds an attribute to the current layout.
     * @param attribute - The attribute to add.
     */
    handleAddToLayout(attribute: AttributeSchema): void {
      this.layoutStore.addAttribute(attribute.key);
    },
  },
});
</script>
