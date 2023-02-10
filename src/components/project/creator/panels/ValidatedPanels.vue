<template>
  <v-container>
    <v-row>
      <slot name="panels" />
    </v-row>
    <v-row align="center" class="mx-auto width-fit">
      <v-col>
        <v-btn
          color="primary"
          :disabled="isButtonDisabled"
          data-cy="button-create-panel"
          @click="emit('add')"
        >
          Create new {{ itemName }}
        </v-btn>
      </v-col>
      <v-col v-if="showError">
        <typography
          :value="`Requires at least 1 ${itemName}.`"
          :color="errorColor"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
/**
 * Validated upload panels.
 */
export default {
  name: "ValidatedPanels",
};
</script>

<script setup lang="ts">
import { defineProps, defineEmits, computed, watch } from "vue";
import { ThemeColors } from "@/util";
import { Typography } from "@/components/common";

const props = defineProps<{
  itemName: string;
  isValidStates: boolean[];
  showError: boolean;
  defaultValidState: boolean;
  isButtonDisabled?: boolean;
}>();

const emit = defineEmits<{
  (e: "add"): void;
  (e: "upload:valid"): void;
  (e: "upload:invalid"): void;
}>();

const errorColor = ThemeColors.error;

const isValid = computed(() =>
  props.isValidStates.length === 0
    ? props.defaultValidState
    : props.isValidStates.filter((isValid) => !isValid).length === 0
);

watch(
  () => isValid.value,
  (valid) => {
    if (valid) {
      emit("upload:valid");
    } else {
      emit("upload:invalid");
    }
  }
);
</script>
