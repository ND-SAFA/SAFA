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
    <div v-if="showBounds">
      <v-text-field
        filled
        label="Minimum"
        type="number"
        v-model="store.editedAttribute.min"
        :hint="minBoundHint"
      />
      <v-text-field
        filled
        label="Maximum"
        type="number"
        v-model="store.editedAttribute.max"
        :hint="maxBoundHint"
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
import { AttributeSchema, AttributeType } from "@/types";
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
  computed: {
    /**
     * @return Whether this attribute value has bounds.
     */
    showBounds(): boolean {
      return ![AttributeType.date, AttributeType.boolean].includes(
        this.attribute?.type || ""
      );
    },
    /**
     * @return The hint for the min bound.
     */
    minBoundHint(): string {
      return [AttributeType.int, AttributeType.float].includes(
        this.attribute?.type || ""
      )
        ? "The minimum value of this number."
        : "The minimum length of this value.";
    },
    /**
     * @return The hint for the max bound.
     */
    maxBoundHint(): string {
      return [AttributeType.int, AttributeType.float].includes(
        this.attribute?.type || ""
      )
        ? "The maximum value of this number."
        : "The maximum length of this value.";
    },
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
