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
  (e: "update:modelValue", value: string | null): void;
  /**
   * Called when the error message is updated.
   */
  (e: "update:errorMessage", value: string | false): void;
  /**
   * Called when the enter button is pressed.
   */
  (e: "enter"): void;
}>();

const model = useVModel(props, "modelValue");

const errorMessage = computed(() => {
  if (
    model.value &&
    !/^\w+([+.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(model.value)
  ) {
    const error = "E-mail must contain a valid domain.";
    emit("update:errorMessage", error);
    return error;
  } else {
    emit("update:errorMessage", false);
    return props.errorMessage;
  }
});
</script>
