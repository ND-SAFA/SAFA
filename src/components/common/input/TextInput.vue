<template>
  <q-input
    v-model="model"
    filled
    :label="props.label"
    data-cy="input-password"
    :error-message="props.errorMessage || ''"
    :error="showError"
    :class="className"
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
import { useVModel } from "@/hooks";

const props = withDefaults(
  defineProps<{
    /**
     * The model value.
     */
    modelValue: string;
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
  }>(),
  {
    b: "1",
    label: "",
    errorMessage: "",
    class: "",
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

const className = computed(() => {
  if (props.class) {
    return props.class;
  } else if (props.b) {
    return `mb-${props.b}`;
  } else {
    return "";
  }
});

const showError = computed(
  () => !!props.errorMessage && props.errorMessage.length > 0
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
