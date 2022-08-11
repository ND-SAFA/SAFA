<template>
  <v-container>
    <flex-box justify="center">
      <v-btn
        large
        color="primary"
        :disabled="isDisabled"
        :loading="isLoading"
        @click="handleClick"
      >
        <v-icon class="mr-1">mdi-transit-connection-variant</v-icon>
        <span v-if="!hasCredentials">{{ disconnectedTitle }}</span>
        <span v-else>{{ connectedTitle }}</span>
      </v-btn>
    </flex-box>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { FlexBox } from "@/components/common/display";

/**
 * Displays an authentication stepper step.
 *
 * @emits `click` - On button click.
 */
export default Vue.extend({
  name: "GenericStepperAuthentication",
  components: { FlexBox },
  props: {
    hasCredentials: {
      type: Boolean,
      required: true,
    },
    isLoading: {
      type: Boolean,
      required: true,
    },
    disconnectedTitle: {
      type: String,
      required: true,
    },
    connectedTitle: {
      type: String,
      required: true,
    },
  },
  methods: {
    /**
     * Opens the authentication window.
     */
    handleClick(): void {
      this.$emit("click");
    },
  },
  computed: {
    /**
     * Returns whether the button is enabled.
     */
    isDisabled(): boolean {
      return this.hasCredentials || this.isLoading;
    },
  },
});
</script>
