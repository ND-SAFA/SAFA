<template>
  <div>
    <flex-box justify="space-between" b="4">
      <v-btn
        v-if="store.isCustom && store.isUpdate"
        text
        color="error"
        @click="handleDeleteLayout"
      >
        <v-icon class="mr-1">mdi-delete</v-icon>
        Delete
      </v-btn>
      <v-spacer />
      <v-btn :disabled="!store.canSave" color="primary" @click="handleSave">
        <v-icon class="mr-1">mdi-content-save</v-icon>
        Save
      </v-btn>
    </flex-box>
    <v-row dense v-if="store.isCustom">
      <v-col cols="6">
        <v-text-field filled label="Name" v-model="store.editedLayout.name"
      /></v-col>
      <v-col cols="6">
        <artifact-type-input
          multiple
          persistent-hint
          v-model="store.editedLayout.artifactTypes"
          hint="This layout only appears on these types."
      /></v-col>
    </v-row>
    <panel-card>
      <attribute-grid editable :layout="store.editedLayout">
        <template v-slot:item="{ attribute }">
          <v-card outlined class="pa-2 mx-2">
            <flex-box v-if="!!attribute" align="center" justify="space-between">
              <typography :value="attribute.label" />
              <icon-button
                icon-id="mdi-delete"
                tooltip="Remove from layout"
                color="error"
                @click="handleDeleteAttribute(attribute)"
              />
            </flex-box>
            <flex-box v-else justify="space-between" align="center">
              <v-select
                filled
                label="Attribute"
                hide-details
                class="mr-2"
                :items="unusedAttributes"
                item-value="key"
                item-text="label"
                v-model="addedAttribute"
              />
              <v-btn
                :disabled="!addedAttribute"
                text
                color="primary"
                @click="handleAddAttribute"
              >
                <v-icon class="mr-1">mdi-plus</v-icon>
                Include Attribute
              </v-btn>
            </flex-box>
          </v-card>
        </template>
      </attribute-grid>
    </panel-card>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { AttributeLayoutSchema, AttributeSchema } from "@/types";
import { attributeLayoutSaveStore, attributesStore } from "@/hooks";
import { handleDeleteAttributeLayout, handleSaveAttributeLayout } from "@/api";
import {
  AttributeGrid,
  ArtifactTypeInput,
  FlexBox,
  PanelCard,
  Typography,
  IconButton,
} from "@/components/common";

/**
 * Allows for editing attribute layouts.
 *
 * @emits-1 `save` - On attribute layout save.
 */
export default Vue.extend({
  name: "SaveAttributeLayout",
  components: {
    IconButton,
    Typography,
    PanelCard,
    ArtifactTypeInput,
    AttributeGrid,
    FlexBox,
  },
  props: {
    layout: Object as PropType<AttributeLayoutSchema>,
  },
  data() {
    return {
      store: attributeLayoutSaveStore(this.layout?.id || ""),
      addedAttribute: "",
    };
  },
  mounted() {
    this.store.resetLayout(this.layout);
  },
  computed: {
    /**
     * @return All project attributes not currently in the layout.
     */
    unusedAttributes(): AttributeSchema[] {
      const usedKeys = this.store.editedLayout.positions.map(({ key }) => key);

      return attributesStore.attributes.filter(
        ({ key }) => !usedKeys.includes(key)
      );
    },
  },
  methods: {
    /**
     * Saves an attribute layout.
     */
    handleSave() {
      handleSaveAttributeLayout(this.store.editedLayout, this.store.isUpdate, {
        onSuccess: () => this.$emit("save"),
      });
    },
    /**
     * Deletes an attribute layout.
     */
    handleDeleteLayout() {
      handleDeleteAttributeLayout(this.store.editedLayout, {});
    },
    /**
     * Deletes an attribute from the layout.
     */
    handleDeleteAttribute(attribute: AttributeSchema) {
      this.store.deleteAttribute(attribute);
    },
    /**
     * Adds an attribute to the layout.
     */
    handleAddAttribute() {
      this.store.addAttribute(this.addedAttribute);
      this.addedAttribute = "";
    },
  },
});
</script>
