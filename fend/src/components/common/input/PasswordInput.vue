<template>
  <q-input
    v-model="model"
    filled
    :label="props.label"
    :type="showPassword ? 'text' : 'password'"
    data-cy="input-password"
    :error-message="props.errorMessage || ''"
    :error="showError"
    @keydown="handleKeydown"
  >
    <template #append>
      <q-icon
        :name="showPassword ? getIcon('pw-show') : getIcon('pw-hide')"
        tooltip="Toggle show password"
        class="cursor-pointer"
        @click="handleToggle"
      />
    </template>
  </q-input>
</template>

<script lang="ts">
/**
 * A generic password input.
 */
export default {
  name: "PasswordInput",
};
</script>

<script setup lang="ts">
import { withDefaults, ref, computed } from "vue";
import { PasswordInputProps } from "@/types";
import { getIcon } from "@/util";
import { useVModel } from "@/hooks";

const props = withDefaults(defineProps<PasswordInputProps>(), {
  label: "Password",
  errorMessage: "",
});

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

const showPassword = ref(false);
const model = useVModel(props, "modelValue");

const showError = computed(
  () => (props.errorMessage && props.errorMessage.length > 0) || false
);

/**
 * Toggles the password visibility.
 */
function handleToggle() {
  showPassword.value = !showPassword.value;
}

/**
 * Emits an event when enter is clicked.
 */
function handleKeydown(e?: { key: string }) {
  if (e?.key === "Enter") {
    emit("enter");
  }
}
</script>
