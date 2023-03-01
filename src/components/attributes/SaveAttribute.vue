<template>
  <div class="q-my-md">
    <text-input
      v-model="store.editedAttribute.key"
      :disabled="isUpdate"
      data-cy="input-attribute-key"
      label="Key"
      hint="The attribute's id."
    />
    <text-input
      v-model="store.editedAttribute.label"
      label="Label"
      data-cy="input-attribute-label"
      hint="The attribute's display name."
    />
    <select-input
      v-model="store.editedAttribute.type"
      option-to-value
      :disabled="isUpdate"
      data-cy="input-attribute-type"
      label="Attribute Type"
      option-label="name"
      option-value="id"
      :options="typeOptions"
      class="q-mb-md"
    />
    <multiselect-input
      v-if="showOptions"
      v-model="store.editedAttribute.options"
      add-values
      :options="[]"
      label="Options"
      data-cy="input-attribute-options"
      hint="Type in an option and press enter to save."
    />
    <div v-if="showBounds">
      <text-input
        v-model="store.editedAttribute.min"
        label="Minimum"
        data-cy="input-attribute-min"
        type="number"
        :hint="store.minBoundHint"
      />
      <text-input
        v-model="store.editedAttribute.max"
        label="Maximum"
        data-cy="input-attribute-max"
        type="number"
        :hint="store.maxBoundHint"
      />
    </div>
    <flex-box justify="between" t="2">
      <text-button
        v-if="isUpdate"
        label="Delete"
        data-cy="button-delete-attribute"
        text
        icon="delete"
        @click="handleDelete"
      />
      <q-space />
      <text-button
        :disabled="!canSave"
        label="Save"
        data-cy="button-save-attribute"
        icon="save"
        @click="handleSave"
      />
    </flex-box>
  </div>
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
import { computed, onMounted, ref, watch } from "vue";
import { AttributeSchema } from "@/types";
import { attributeTypeOptions } from "@/util";
import { attributeSaveStore } from "@/hooks";
import { handleDeleteAttribute, handleSaveAttribute } from "@/api";
import {
  FlexBox,
  TextButton,
  TextInput,
  SelectInput,
  MultiselectInput,
} from "@/components/common";

const props = defineProps<{
  attribute?: AttributeSchema;
}>();

const emit = defineEmits<{
  (e: "save"): void;
}>();

const typeOptions = attributeTypeOptions();
const store = ref(attributeSaveStore(props.attribute?.key || ""));

const isUpdate = computed(() => store.value.isUpdate);
const showOptions = computed(() => store.value.showOptions);
const showBounds = computed(() => store.value.showBounds);
const canSave = computed(() => store.value.canSave);

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
