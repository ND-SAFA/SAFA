<template>
  <v-container>
    <v-text-field
      filled
      :disabled="store.isUpdate"
      label="Key"
      v-model="store.editedAttribute.key"
      hint="The unique key that this attribute is saved under."
    />
    <v-text-field
      filled
      label="Label"
      v-model="store.editedAttribute.label"
      hint="The label that is displayed for this attribute."
    />
    <v-select
      filled
      :disabled="store.isUpdate"
      label="Attribute Type"
      v-model="store.editedAttribute.type"
      item-text="name"
      item-value="id"
      :items="typeOptions"
    />
    <v-combobox
      v-if="store.editedAttribute.type.includes('select')"
      filled
      chips
      deletable-chips
      multiple
      label="Options"
      v-model="store.editedAttribute.options"
      hint="Type in an option and press enter to save."
    />
    <flex-box justify="space-between">
      <v-btn v-if="store.isUpdate" text color="error" @click="handleDelete">
        <v-icon class="mr-1">mdi-delete</v-icon>
        Delete
      </v-btn>
      <v-spacer />
      <v-btn :disabled="!store.canSave" color="primary" @click="handleSave">
        <v-icon class="mr-1">mdi-content-save</v-icon>
        Save
      </v-btn>
    </flex-box>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { AttributeSchema } from "@/types";
import { attributeTypeOptions } from "@/util";
import { attributeSaveStore } from "@/hooks";
import { FlexBox } from "@/components/common";

/**
 * Allows for creating and editing attributes.
 */
export default Vue.extend({
  name: "SaveAttribute",
  components: { FlexBox },
  props: {
    attribute: Object as PropType<AttributeSchema>,
  },
  data() {
    return {
      typeOptions: attributeTypeOptions(),
      store: attributeSaveStore(this.attribute?.key || ""),
    };
  },
  mounted() {
    this.store.resetAttribute(this.attribute);
  },
  methods: {
    /**
     * Saves an attribute.
     */
    handleSave() {
      //TODO
    },
    /**
     * Deletes an attribute.
     */
    handleDelete() {
      //TODO
    },
  },
  watch: {
    /**
     * Update the base attribute if it changes.
     */
    attribute() {
      this.store.resetAttribute(this.attribute);
    },
  },
});
</script>
