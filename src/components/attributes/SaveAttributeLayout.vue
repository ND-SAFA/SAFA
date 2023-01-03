<template>
  <div>
    <v-row dense v-if="store.isCustom">
      <v-col cols="6">
        <v-text-field filled label="Name" v-model="store.editedLayout.name"
      /></v-col>
      <v-col cols="6">
        <artifact-type-input
          multiple
          persistent-hint
          v-model="store.editedLayout.artifactTypes"
          hint="The layout will only appear on these artifact types."
          :error-messages="store.typeErrors"
      /></v-col>
    </v-row>

    <panel-card>
      <attribute-grid editable :layout="store.editedLayout">
        <template v-slot:item="{ attribute }">
          <v-card v-if="!!attribute" outlined class="pa-3 mx-2">
            <flex-box align="center" justify="space-between">
              <div>
                <typography :value="attribute.label" />
                <br />
                <typography variant="caption" :value="attribute.key" />
              </div>
              <icon-button
                icon-id="mdi-delete"
                tooltip="Remove from layout"
                color="error"
                @click="handleDeleteAttribute(attribute)"
              />
            </flex-box>
          </v-card>
        </template>
      </attribute-grid>
    </panel-card>

    <flex-box justify="space-between" b="4">
      <text-button
        v-if="store.isCustom && store.isUpdate"
        text
        variant="delete"
        @click="handleDeleteLayout"
      >
        Delete
      </text-button>
      <v-spacer />
      <text-button
        :disabled="!store.canSave"
        variant="save"
        @click="handleSave"
      >
        Save
      </text-button>
    </flex-box>
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
  TextButton,
} from "@/components/common";

/**
 * Allows for editing attribute layouts.
 *
 * @emits-1 `save` - On attribute layout save.
 */
export default Vue.extend({
  name: "SaveAttributeLayout",
  components: {
    TextButton,
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
  watch: {
    /**
     * Updates the store when the layout changes.
     */
    layout(): void {
      this.store = attributeLayoutSaveStore(this.layout?.id || "");
    },
  },
});
</script>
