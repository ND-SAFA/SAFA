<template>
  <v-container>
    <v-text-field
      filled
      :disabled="isUpdate"
      label="Key"
      v-model="editedAttribute.key"
    />
    <v-text-field filled label="Label" v-model="editedAttribute.label" />
    <v-select
      filled
      :disabled="isUpdate"
      label="Type"
      v-model="editedAttribute.type"
      item-text="name"
      item-value="id"
      :items="typeOptions"
    />
    <v-combobox
      v-if="editedAttribute.type.includes('select')"
      filled
      chips
      deletable-chips
      multiple
      label="Options"
      v-model="editedAttribute.options"
    />
    <flex-box justify="space-between">
      <v-btn v-if="isUpdate" text color="error" @click="handleDelete">
        <v-icon class="mr-1">mdi-delete</v-icon>
        Delete
      </v-btn>
      <v-spacer />
      <v-btn color="primary" @click="handleSave">
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
  computed: {
    /**
     * @return  The attribute being edited.
     */
    editedAttribute(): AttributeSchema {
      return this.store.editedAttribute;
    },
    /**
     * @return  Whether the attribute can be saved.
     */
    canSave(): boolean {
      return this.store.canSave;
    },
    /**
     * @return Whether an existing attribute is being updated.
     */
    isUpdate(): boolean {
      return this.store.isUpdate;
    },
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
