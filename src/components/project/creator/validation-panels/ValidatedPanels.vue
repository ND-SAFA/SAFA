<template>
  <v-container>
    <v-row>
      <v-expansion-panels>
        <slot name="panels" />
      </v-expansion-panels>
    </v-row>
    <v-row align="center" class="mx-auto" style="width: fit-content">
      <v-col>
        <v-btn
          color="primary"
          :disabled="isButtonDisabled"
          @click="$emit('onAdd')"
        >
          Create new {{ itemName }}</v-btn
        >
      </v-col>
      <v-col v-if="showError" style="white-space: nowrap">
        Requires at least 1 {{ itemName }}.
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ThemeColors } from "@/util";

export default Vue.extend({
  props: {
    itemName: {
      type: String,
      required: true,
    },
    isValidStates: {
      type: Array as PropType<boolean[]>,
      required: true,
    },
    showError: {
      type: Boolean,
      required: true,
    },
    defaultValidState: {
      type: Boolean,
      required: true,
    },
    isButtonDisabled: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    errorColor(): string {
      return ThemeColors.error;
    },
    isValid(): boolean {
      if (this.isValidStates.length === 0) return this.defaultValidState;
      return this.isValidStates.filter((isValid) => !isValid).length === 0;
    },
  },
  watch: {
    isValid(isValid: boolean): void {
      if (isValid) {
        this.$emit("onIsValid");
      } else {
        this.$emit("onIsInvalid");
      }
    },
  },
});
</script>
