<template>
  <text-input
    v-model="model"
    :label="props.label || 'Email'"
    :error-message="errorMessage"
    @enter="emit('enter')"
  />
</template>

<script lang="ts">
/**
 * An input for email addresses.
 */
export default {
  name: "EmailInput",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { useVModel } from "@/hooks";
import TextInput from "./TextInput.vue";

const props = defineProps<{
  modelValue: string;
  errorMessage?: string | false;
  label?: string;
}>();

const emit = defineEmits<{
  /**
   * Called when the email is updated.
   */
  (e: "update:modelValue", value: string | number | null): void;
  /**
   * Called when the enter button is pressed.
   */
  (e: "enter"): void;
}>();

const model = useVModel(props, "modelValue");

const errorMessage = computed(() => {
  const domain = model.value.split("@")[1];

  if (!model.value) {
    return props.errorMessage;
  }

  if (!domain) {
    return "Email must contain an @ symbol and domain.";
  }

  return props.errorMessage;
});
</script>
