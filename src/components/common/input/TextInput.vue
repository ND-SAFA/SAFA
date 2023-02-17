<template>
  <q-input
    v-model="model"
    filled
    :label="label"
    data-cy="input-password"
    :error-message="errorMessage || ''"
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
import { defineProps, defineEmits, withDefaults, computed } from "vue";
import { SizeType } from "@/types";
import { useVModel } from "@/hooks";

const props = withDefaults(
  defineProps<{
    modelValue: string;
    label?: string;
    errorMessage?: string | false;
    b?: SizeType;
    class?: string;
  }>(),
  {
    b: "1",
    label: "",
    errorMessage: "",
    class: "",
  }
);

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
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
