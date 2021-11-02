<template>
  <v-container>
    <v-row>
      <v-expansion-panels :value="0">
        <slot name="panels" />
      </v-expansion-panels>
    </v-row>
    <v-row justify="center" class="mt-5">
      <v-container>
        <v-row
          v-if="showError"
          justify="center"
          style="color: red"
          class="mb-10"
        >
          <label>{{ noItemError }}</label>
        </v-row>
        <v-row justify="center">
          <v-btn @click="$emit('onAdd')" small fab color="secondary">
            <v-icon> mdi-plus </v-icon>
          </v-btn>
        </v-row>
      </v-container>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

export default Vue.extend({
  props: {
    isValidStates: {
      type: Array as PropType<boolean[]>,
      required: true,
    },
    noItemError: {
      type: String,
      required: true,
    },
    showError: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    isValid(): boolean {
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
