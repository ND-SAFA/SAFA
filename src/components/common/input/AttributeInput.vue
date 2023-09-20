<template>
  <text-input
    v-if="attribute.type === 'text'"
    :label="attribute.label"
    :rules="[lengthRules]"
    :model-value="attributes[attribute.key] as string"
    @update:model-value="handleInput"
  />

  <text-input
    v-else-if="attribute.type === 'paragraph'"
    type="textarea"
    :label="attribute.label"
    :rules="[lengthRules]"
    :model-value="attributes[attribute.key] as string"
    @update:model-value="handleInput"
  />

  <select-input
    v-else-if="attribute.type === 'select'"
    :label="attribute.label"
    :options="attribute.options || []"
    :model-value="attributes[attribute.key] as string"
    @update:model-value="handleInput"
  />

  <multiselect-input
    v-else-if="attribute.type === 'multiselect'"
    :label="attribute.label"
    :options="attribute.options || []"
    :rules="[lengthRules]"
    :model-value="attributes[attribute.key] as string[]"
    @update:model-value="handleInput as (value: string[]) => void"
  />

  <artifact-input
    v-else-if="attribute.type === 'relation'"
    multiple
    :label="attribute.label"
    :rules="[lengthRules]"
    :model-value="attributes[attribute.key] as string[]"
    @update:model-value="handleInput"
  />

  <text-input
    v-else-if="attribute.type === 'int'"
    type="number"
    :label="attribute.label"
    :rules="[intRules, numRules]"
    :model-value="attributes[attribute.key] as number"
    @update:model-value="handleInput"
  />

  <text-input
    v-else-if="attribute.type === 'float'"
    type="number"
    :label="attribute.label"
    :rules="[numRules]"
    :model-value="attributes[attribute.key] as number"
    @update:model-value="handleInput"
  />

  <q-checkbox
    v-else-if="attribute.type === 'boolean'"
    :label="attribute.label"
    :model-value="attributes[attribute.key]"
    class="q-my-sm"
    @update:model-value="handleInput"
  />

  <q-input
    v-else-if="attribute.type === 'date'"
    filled
    :label="attribute.label"
    :model-value="attributes[attribute.key] as string"
    @update:model-value="handleInput"
  >
    <template #append>
      <q-icon :name="getIcon('calendar')" class="cursor-pointer">
        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
          <q-date
            :model-value="attributes[attribute.key]"
            mask="YYYY-MM-DDTHH:mm:00.000Z"
            @update:model-value="handleInput"
          >
            <div class="row items-center justify-end">
              <q-btn v-close-popup label="Close" color="primary" flat />
            </div>
          </q-date>
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>

<script lang="ts">
/**
 * An input for a generic attribute.
 */
export default {
  name: "AttributeInput",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { AttributeDataType, AttributeInputProps } from "@/types";
import { getIcon } from "@/util";
import TextInput from "./TextInput.vue";
import SelectInput from "./SelectInput.vue";
import ArtifactInput from "./ArtifactInput.vue";
import MultiselectInput from "./MultiselectInput.vue";

const props = defineProps<AttributeInputProps>();

const intRules = computed(
  () =>
    (value: string | number | undefined): string | true => {
      if (value === undefined || value === "") {
        return true;
      } else {
        const strValue = typeof value === "string" ? value : String(value);

        return strValue.includes(".") ? "Must be a valid integer." : true;
      }
    }
);

const numRules = computed(
  () =>
    (value: string | number | undefined): string | true => {
      const { min = null, max = null } = props.attribute;
      const numValue = typeof value === "string" ? parseFloat(value) : value;

      if (numValue === undefined || isNaN(numValue)) {
        return true;
      } else if (max !== null && numValue > max) {
        return `Value is greater than ${max}.`;
      } else if (min !== null && numValue < min) {
        return `Value is less than ${min}.`;
      } else {
        return true;
      }
    }
);

const lengthRules = computed(
  () =>
    (value: string | string[] | undefined): string | true => {
      const { min = null, max = null } = props.attribute;
      const unit = Array.isArray(value) ? "items" : "characters";

      if (!value) {
        return true;
      } else if (max !== null && value.length > max) {
        return `Value has greater than ${max} ${unit}.`;
      } else if (min !== null && value.length < min) {
        return `Value has less than ${min} ${unit}.`;
      } else {
        return true;
      }
    }
);

/**
 * Handles input changes to make adjustments to the stored data types.
 *
 * @param value - The updated value of this attribute.
 */
function handleInput(value: AttributeDataType): void {
  if (props.attribute.type === "int") {
    props.attributes[props.attribute.key] = parseInt(String(value));
  } else if (props.attribute.type === "float") {
    props.attributes[props.attribute.key] = parseFloat(String(value));
  } else if (props.attribute.type === "date") {
    props.attributes[props.attribute.key] = new Date(
      String(value)
    ).toISOString();
  } else {
    props.attributes[props.attribute.key] = value;
  }
}
</script>
