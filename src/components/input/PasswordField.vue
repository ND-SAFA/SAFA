<template>
  <v-text-field
    filled
    label="Password"
    v-model="model"
    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
    :type="showPassword ? 'text' : 'password'"
    @click:append="showPassword = !showPassword"
  />
</template>

<script lang="ts">
import Vue from "vue";

/**
 * A generic password input.
 */
export default Vue.extend({
  name: "password-field",
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
    model(currentValue: string) {
      this.$emit("input", currentValue);
    },
  },
});
</script>
