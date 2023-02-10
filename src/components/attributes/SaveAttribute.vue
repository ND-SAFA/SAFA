<template>
  <v-container>
    <v-text-field
      v-model="store.editedAttribute.key"
      filled
      :disabled="store.isUpdate"
      data-cy="input-attribute-key"
      label="Key"
      hint="The unique key that this attribute is saved under."
    />
    <v-text-field
      v-model="store.editedAttribute.label"
      filled
      label="Label"
      data-cy="input-attribute-label"
      hint="The label that is displayed for
    this attribute."
    />
    <v-select
      v-model="store.editedAttribute.type"
      filled
      :disabled="store.isUpdate"
      data-cy="input-attribute-type"
      label="Attribute Type"
      item-text="name"
      item-value="id"
      :items="typeOptions"
    />
    <v-combobox
      v-if="store.showOptions"
      v-model="store.editedAttribute.options"
      filled
      chips
      deletable-chips
      multiple
      label="Options"
      data-cy="input-attribute-options"
      hint="Type in an option and press enter to save."
    />
    <div v-if="store.showBounds">
      <v-text-field
        v-model="store.editedAttribute.min"
        filled
        label="Minimum"
        data-cy="input-attribute-min"
        type="number"
        :hint="store.minBoundHint"
      />
      <v-text-field
        v-model="store.editedAttribute.max"
        filled
        label="Maximum"
        data-cy="input-attribute-max"
        type="number"
        :hint="store.maxBoundHint"
      />
    </div>
    <flex-box justify="space-between">
      <text-button
        v-if="store.isUpdate"
        data-cy="button-delete-attribute"
        text
        variant="delete"
        @click="handleDelete"
      >
        Delete
      </text-button>
      <v-spacer />
      <text-button
        :disabled="!store.canSave"
        data-cy="button-save-attribute"
        variant="save"
        @click="handleSave"
      >
        Save
      </text-button>
    </flex-box>
  </v-container>
</template>

<script lang="ts">
/**
 * Allows for creating and editing attributes.
 */
export default {
  name: "SaveAttribute",
};
</script>

<script setup lang="ts">
import { onMounted, ref, watch, defineProps, defineEmits } from "vue";
import { AttributeSchema } from "@/types";
import { attributeTypeOptions } from "@/util";
import { attributeSaveStore } from "@/hooks";
import { handleDeleteAttribute, handleSaveAttribute } from "@/api";
import { FlexBox, TextButton } from "@/components/common";

const props = defineProps<{
  attribute?: AttributeSchema;
}>();

const emit = defineEmits<{
  (e: "save"): void;
}>();

const typeOptions = attributeTypeOptions();
const store = ref(attributeSaveStore(props.attribute?.key || ""));

/**
 * Saves an attribute.
 */
function handleSave() {
  handleSaveAttribute(store.value.editedAttribute, store.value.isUpdate, {
    onSuccess: () => emit("save"),
  });
}

/**
 * Deletes an attribute.
 */
function handleDelete() {
  handleDeleteAttribute(store.value.editedAttribute, {});
}

onMounted(() => store.value.resetAttribute(props.attribute));

watch(
  () => props.attribute,
  () => store.value.resetAttribute(props.attribute)
);
</script>
