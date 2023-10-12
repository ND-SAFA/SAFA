<template>
  <q-input
    v-model="model"
    filled
    :label="props.label"
    :data-cy="props.dataCy"
    :error-message="props.errorMessage || ''"
    :error="showError"
    :class="className"
    :hint="props.hint"
    :hide-hint="props.hideHint"
    :type="props.type"
    :disable="props.disabled"
    @keydown="handleKeydown"
  >
    <template #append>
      <slot name="append" />
    </template>
  </q-input>
</template>

<script lang="ts">
/**
 * A generic text input.
 */
export default {
  name: "TextInput",
};
</script>

<script setup lang="ts">
import { withDefaults, computed } from "vue";
import { TextInputProps } from "@/types";
import { useMargins, useVModel } from "@/hooks";

const props = withDefaults(defineProps<TextInputProps>(), {
  modelValue: undefined,
  b: "1",
  label: "",
  errorMessage: "",
  class: "",
  hint: undefined,
  type: "text",
  dataCy: undefined,
});

const emit = defineEmits<{
  /**
   * Called when the model is updated.
   */
  (e: "update:modelValue", value: string | number | null): void;
  /**
   * Called when the enter button is pressed.
   */
  (e: "enter"): void;
}>();

const model = useVModel(props, "modelValue");

const className = useMargins(props, () => [[!!props.class, props.class]]);

const showError = computed(() =>
  props.hideHint
    ? // If the hint is hidden, don't show the error. Undefined will remove the bottom margin for the message.
      undefined
    : // If there is an error message, show it. Either way, the input will have a bottom margin.
      (props.errorMessage && props.errorMessage.length > 0) || false
);

/**
 * Emits an event when enter is clicked.
 */
function handleKeydown(e?: { key: string }) {
  if (e?.key === "Enter") {
    emit("enter");
  }
}
</script>
