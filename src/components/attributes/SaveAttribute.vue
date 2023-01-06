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
      v-if="store.showOptions"
      filled
      chips
      deletable-chips
      multiple
      label="Options"
      v-model="store.editedAttribute.options"
      hint="Type in an option and press enter to save."
    />
    <div v-if="store.showBounds">
      <v-text-field
        filled
        label="Minimum"
        type="number"
        v-model="store.editedAttribute.min"
        :hint="store.minBoundHint"
      />
      <v-text-field
        filled
        label="Maximum"
        type="number"
        v-model="store.editedAttribute.max"
        :hint="store.maxBoundHint"
      />
    </div>
    <flex-box justify="space-between">
      <text-button
        v-if="store.isUpdate"
        text
        variant="delete"
        @click="handleDelete"
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
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { AttributeSchema } from "@/types";
import { attributeTypeOptions } from "@/util";
import { attributeSaveStore } from "@/hooks";
import { handleDeleteAttribute, handleSaveAttribute } from "@/api";
import { FlexBox, TextButton } from "@/components/common";

/**
 * Allows for creating and editing attributes.
 *
 * @emits-1 `save` - On attribute save.
 */
export default Vue.extend({
  name: "SaveAttribute",
  components: { TextButton, FlexBox },
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
      handleSaveAttribute(this.store.editedAttribute, this.store.isUpdate, {
        onSuccess: () => this.$emit("save"),
      });
    },
    /**
     * Deletes an attribute.
     */
    handleDelete() {
      handleDeleteAttribute(this.store.editedAttribute, {});
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
