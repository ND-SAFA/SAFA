<template>
  <v-text-field
    v-model="model"
    filled
    :label="label"
    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
    :type="showPassword ? 'text' : 'password'"
    data-cy="input-password"
    :error-messages="errors"
    :error="errors.length > 0"
    @click:append="showPassword = !showPassword"
    @keydown.enter="emit('enter')"
  />
</template>

<script lang="ts">
/**
 * A generic password input.
 */
export default {
  name: "PasswordField",
};
</script>

<script setup lang="ts">
import { defineProps, defineEmits, withDefaults, ref } from "vue";
import { useVModel } from "@/hooks";

const props = withDefaults(
  defineProps<{
    modelValue: string;
    label?: string;
    errors?: string[];
  }>(),
  { label: "Password", errors: undefined }
);

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
  (e: "enter"): void;
}>();

const showPassword = ref(false);
const model = useVModel(props, "modelValue");
</script>
