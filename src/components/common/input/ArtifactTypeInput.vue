<template>
  <v-combobox
    ref="artifactTypeInput"
    v-model="model"
    filled
    :label="label"
    :multiple="!!multiple"
    :items="typeOptionsStore.artifactTypes"
    :hint="hint"
    :hide-details="hideDetails"
    :persistent-hint="persistentHint"
    :error-messages="errorMessages"
    item-text="label"
    item-value="type"
    @blur="emit('blur')"
    @submit="emit('blur')"
  >
    <template #append>
      <icon-button
        small
        icon-id="mdi-content-save-outline"
        tooltip="Save Types"
        data-cy="button-save-types"
        @click="handleClose"
      />
    </template>
    <template #selection="{ item }">
      <attribute-chip artifact-type :value="item" />
    </template>
  </v-combobox>
</template>

<script lang="ts">
/**
 * An input for selecting artifact types.
 */
export default {
  name: "ArtifactTypeInput",
};
</script>

<script setup lang="ts">
import { computed, ref, withDefaults, defineProps, defineEmits } from "vue";
import { typeOptionsStore, useVModel } from "@/hooks";
import { IconButton } from "@/components/common/button";
import { AttributeChip } from "@/components/common/display";

const props = withDefaults(
  defineProps<{
    modelValue: string[] | string | null;
    multiple?: boolean;
    label?: string;
    hint?: string;
    persistentHint?: boolean;
    hideDetails?: boolean;
    errorMessages?: string[];
  }>(),
  {
    label: "Artifact Types",
    multiple: false,
    hint: undefined,
    errorMessages: undefined,
  }
);

const emit = defineEmits<{
  (e: "update:modelValue", value: string[] | string | null): void;
  (e: "blur"): void;
}>();

const artifactTypeInput = ref<HTMLElement | null>(null);

const model = useVModel(props, "modelValue");

/**
 * Closes the selection window.
 */
function handleClose(): void {
  artifactTypeInput.value?.blur();
}
</script>
