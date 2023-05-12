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
  />
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
import { SizeType } from "@/types";
import { useMargins, useVModel } from "@/hooks";

const props = withDefaults(
  defineProps<{
    /**
     * The model value.
     */
    modelValue?: string | number | null;
    /**
     * An error message to display, if one exists.
     */
    errorMessage?: string | false;
    /**
     * The classnames to include on this component.
     */
    class?: string;
    /**
     * The label to display.
     */
    label?: string;
    /**
     * The bottom margin.
     */
    b?: SizeType;
    /**
     * A hint to display below the input.
     */
    hint?: string;
    /**
     * Whether to hide the hint.
     */
    hideHint?: boolean;
    type?:
      | "text"
      | "password"
      | "textarea"
      | "email"
      | "search"
      | "tel"
      | "file"
      | "number"
      | "url"
      | "time"
      | "date";
    /**
     * Whether to disable this input.
     */
    disabled?: boolean;
    /**
     * A testing selector.
     */
    dataCy?: string;
  }>(),
  {
    modelValue: undefined,
    b: "1",
    label: "",
    errorMessage: "",
    class: "",
    hint: undefined,
    type: "text",
    dataCy: undefined,
  }
);

const emit = defineEmits<{
  /**
   * Called when the model is updated.
   */
  (e: "update:modelValue"): void;
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
      !!props.errorMessage && props.errorMessage.length > 0
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
