<template>
  <v-text-field
    v-model="model"
    filled
    :label="label"
    :type="showPassword ? 'text' : 'password'"
    data-cy="input-password"
    :error-messages="errors"
    :error="errors && errors.length > 0"
    @keydown.enter="emit('enter')"
  >
    <template #append-inner>
      <icon-button
        small
        :icon-id="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        tooltip="Toggle show password"
        @click="handleToggle"
      />
    </template>
  </v-text-field>
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
import IconButton from "@/components/common/button/IconButton.vue";

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

/**
 * Toggles the password visibility.
 */
function handleToggle() {
  showPassword.value = !showPassword.value;
}
</script>
