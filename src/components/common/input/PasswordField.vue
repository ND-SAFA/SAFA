<template>
  <v-text-field
    filled
    label="Password"
    v-model="model"
    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
    :type="showPassword ? 'text' : 'password'"
    data-cy="input-password"
    @click:append="showPassword = !showPassword"
    @keydown.enter="$emit('enter')"
  />
</template>

<script lang="ts">
import Vue from "vue";

/**
 * A generic password input.
 *
 * @emits `input` (string) - On input change.
 * @emits `enter` - On submit.
 */
export default Vue.extend({
  name: "PasswordField",
  props: {
    value: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      model: this.value,
      showPassword: false,
    };
  },
  watch: {
    /**
     * Updates the model if the value changes.
     */
    value(currentValue: string) {
      this.model = currentValue;
    },
    /**
     * Emits changes to the model.
     */
    model(currentValue: string) {
      this.$emit("input", currentValue);
    },
  },
});
</script>
