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
        :name="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
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
     * The label to display.
     */
    label?: string;
  }>(),
  {
    label: "Password",
    errorMessage: "",
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

const showPassword = ref(false);
const model = useVModel(props, "modelValue");

const showError = computed(
  () => !!props.errorMessage && props.errorMessage.length > 0
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
